from pymongo import MongoClient
from Meowbot.services.template_mongodb import MongoDbCtxTemplate

class UserManager(MongoDbCtxTemplate):

    def __init__(self, client: MongoClient, name: str=None) -> None:
        super().__init__(client, name)
        self._db = client['linebot-foxbox']

    # 獲取所有用戶資料
    def get_all_users(self):

        # 獲取 集合
        collection_users = self._db["Users"]
        users = collection_users.find({}) # 查詢全部

        # 遍歷並處理每個文檔
        for user in users:
            print(f'User: {user["UserID"]}')