"""CLI chatbot manager"""

from .base_chatbot import BaseChatbotGenerator

class CliChatbotGenerator(BaseChatbotGenerator):
    """CLI chatbot manager"""

    def get_templates(self):
        return {
            # pylint: disable=line-too-long
            'langchain-chatbot-basic': 'https://github.com/corby-templates/langchain-chatbot-basic.git',
            'langchain-chatbot-tools': 'https://github.com/corby-templates/langchain-chatbot-tools.git',
            'langchain-huggingface-chatbot': 'https://github.com/corby-templates/langchain-huggingface-chatbot'
    }
