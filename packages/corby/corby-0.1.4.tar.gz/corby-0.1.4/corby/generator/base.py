"""Base class to be extended by each generator"""

import os
import shutil
from abc import ABC
from jinja2 import Environment, FileSystemLoader, Undefined
import inquirer
import git

class BaseGenerator(ABC):
    '''Abstract class to be extended by each generator'''

    def replace_in_file(self, file_path, params):
        '''Replace the placeholders in a file with the given params'''

        env = Environment(loader=FileSystemLoader(os.path.dirname(file_path)))
        # pylint: disable=too-few-public-methods
        class SilentUndefined(Undefined):
            '''Custom handler for undefined variables in jinja2'''
            def _fail_with_undefined_error(self, *args, **kwargs):
                return ''
        env.undefined = SilentUndefined
        template = env.get_template(os.path.basename(file_path))
        rendered_template = template.render(params=params)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(rendered_template)

    def replace_in_folder(self, folder_path, params):
        '''Runs replace_in_file for each file in the given folder'''
        # pylint: disable=unused-variable
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.replace_in_file(file_path, params)

    def get_templates(self):
        '''Returns a dictionary with the available templates for the generator'''
        raise NotImplementedError

    def ask_template(self):
        '''Ask the user to select a template from the list returned by get_templates'''
        templates = self.get_templates()

        templates_names = list(templates.keys())
        templates_names.append("Other")

        questions = [
            inquirer.List(
                "template", 
                message="Select one of the available templates:",
                choices=templates_names
            ),
        ]

        answers = inquirer.prompt(questions)

        if answers["template"] == "Other":
            template_url_question = [
                inquirer.Text(
                    "template_url", 
                    message="Enter the URL of the template's repository:"
                ),
            ]
            template_url_answers = inquirer.prompt(template_url_question)
            template_url = template_url_answers["template_url"]
            template_name = template_url.split("/")[-1].split(".")[0]
        else:
            template_url = templates[answers["template"]]
            template_name = answers["template"]

        return {
            "template_name": template_name,
            "template_url": template_url
        }

    def clone_template(self, template_url, template_name):
        '''Download a template from github and extract the skeleton'''

        # Clone the template
        git.Repo.clone_from(template_url, os.getcwd() + '/' + template_name)

    def extract_skeleton(self, template_name):
        '''Extract the template skeleton'''
        shutil.move(
            os.getcwd() + '/' + template_name + '/skeleton', os.getcwd() + '/skeleton'
        )

    def ask_template_inputs(self, template_path):
        '''Asks the user the inputs.json questions in the template's folder'''
        if os.path.isfile(template_path + '/inputs.json'):
            with open(template_path + '/inputs.json', 'r', encoding='utf-8') as schema:
                questions = inquirer.load_from_json(schema.read())
                answers = inquirer.prompt(questions)
                return answers
        return {}

    def cleanup(self, template_name):
        '''Removes the base folder from the template'''
        shutil.rmtree(os.getcwd() + '/' + template_name)

    def get_generator_params(self, name):
        '''Returns a dictionary with the parameters to be replaced in the template'''
        raise NotImplementedError

    def create(self, name):
        '''Generates a new entity'''
        app_path = os.getcwd() + '/' + name
        selected_template = self.ask_template()
        template_params = {}
        try:
            generator_params = self.get_generator_params(name)
        except NotImplementedError:
            generator_params = {}
        template_params.update(generator_params)
        self.clone_template(selected_template["template_url"], selected_template["template_name"])
        template_custom_inputs = self.ask_template_inputs(selected_template["template_name"])
        if bool(template_custom_inputs):
            template_params.update(template_custom_inputs)
        self.replace_in_folder(
            selected_template["template_name"] + '/skeleton',
            template_params
        )
        self.extract_skeleton(selected_template["template_name"])
        os.rename(os.getcwd() + '/skeleton', app_path)
        self.cleanup(selected_template["template_name"])
        print("Yeepay 🎉, your project is ready!")
        print("You can find it in the " + name + " folder")
