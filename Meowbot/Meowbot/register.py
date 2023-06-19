from pymongo import MongoClient
from Meolask.meolask import Meolask
from Meolask.template import RegisterTemplate
from Meowbot.controllers.linebot_view import Service as LinebotService
from Meowbot.service import MongoDbCtxType, ServiceType
from Meowbot.services.meowlibot.meowlibot import Agent as LinebotAgent_Meowlibot

from settings import (
    LINE_BOT_CHANNEL_ACCESS_TOKEN,
    LINE_BOT_CHANNEL_SECRET
)

# 引入：資料庫上下文
from Meowbot.databases.mongodb.user_manager import UserManager
from Meowbot.databases.mongodb.group_manager import GroupManager
# More...

# 引入：控制器
from Meowbot.controllers.linebot_view import linebot_view as LinebotController
# More...

# 資料庫上下文注冊器 (MongoDB)
class MongoDbContexts(RegisterTemplate):

    # [Abs:Override]：注冊器
    def register(self, app: Meolask, db: MongoClient) -> None:

        # MongoDB
        app.register_mongodbCtx({
            MongoDbCtxType.UserManager: UserManager(db),
            MongoDbCtxType.GroupManager: GroupManager(db)
            # More...
        })


# 一般控制器注冊
class Controllers(RegisterTemplate):

    # [Abs:Override]：注冊器
    def register(self, app: Meolask) -> None:
        app.register_view(LinebotController, '/api/linebot', services = {
            ServiceType.LinebotAgent_Meowlibot:         # 索引值(用於查詢服務)
            LinebotService(
                LINE_BOT_CHANNEL_SECRET,                # Line-bot >> 密鑰
                LINE_BOT_CHANNEL_ACCESS_TOKEN,          # Line-bot >> 訪問令牌(金鑰)
                LinebotAgent_Meowlibot(                 # Agent >> 服務代理：提供服務的對象
                    ServiceType.LinebotAgent_Meowlibot  # Agent >> 記錄索引值
                )
            )
            # More... LineBot-Agent
        })
        # More...
