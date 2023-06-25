'''
Chat GPT
'''

from Meolask.template import ServiceTemplate
from MeowkitPy.logging.logger import log
from enum import Enum, auto
import json, requests

# ChatGPT 服務 >> 注冊時創建
class Service(ServiceTemplate):

    # 建構式
    def __init__(self, id: str, endpoint_url: str, key: str, model: str, name: str=None) -> None:
        super().__init__(id, name)
        self._endpoint_url = endpoint_url    # ChatGPT >> 終端連結
        self._key = key                      # ChatGPT >> 訪問令牌(金鑰)
        self._model = model                  # ChatGPT >> 模型版本

    # 發送請求
    def handle(self, msg: str) -> str:
        return requests.post(
            self._endpoint_url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._key}',
            },
            json={
                'model': f'{self._model}',
                'messages': [
                    {'role': 'user', 'content': f"{msg}"},
                    {'role': 'assistant', 'content': ""}
                ],
                'temperature': 0.8,
                'max_tokens': 512,
            }
        )
