from pymongo import MongoClient
from Meowbot.services.template_mongodb import MongoDbCtxTemplate

class GroupManager(MongoDbCtxTemplate):

    def __init__(self, client: MongoClient, name: str=None) -> None:
        super().__init__(client, name)
        self._db = client['linebot-foxbox']

    # 獲取所有用戶資料
    def get_all_group(self):
        print('DBTest')
        pass
