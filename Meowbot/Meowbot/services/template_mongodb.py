from pymongo import MongoClient
from Meolask.template import ServiceTemplate

class MongoDbCtxTemplate(ServiceTemplate):
    
    def __init__(self, client: MongoClient, name: str=None) -> None:
        super().__init__(name)
        self._client = client
