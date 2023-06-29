from pymongo import MongoClient
from Meolask.modules.service import ServiceTemplate

class MongoDbCtxTemplate(ServiceTemplate):
    
    def __init__(self, client: MongoClient, id: str, name: str=None) -> None:
        super().__init__(id, name)
        self._client = client
