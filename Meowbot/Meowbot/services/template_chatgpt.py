'''
Chat GPT
'''
from Meolask.template import ServiceTemplate
from enum import Enum, auto

class Service(ServiceTemplate):
    def __init__(self, key: str, model: str,
        name: str=None) -> None:
        super().__init__(name)
        self.key = key          # ChatGPT >> 訪問令牌(金鑰)
        self.model = model      # ChatGPT >> 模型版本 >> 'gpt-3.5-turbo'

class ChatGPT():

    def __init__(self, service: Service) -> None:
        self.service = service
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.service.key}'
        }

    def _package(self, msg: str):
        json = {
        'model': self._model,
        'messages': [
            { "role": "user", "content": msg },
            { "role": "assistant", "content": "" }
        ],
    }

    def message(msg: str) -> str:
        pass