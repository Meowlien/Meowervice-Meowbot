﻿import json
from MeowkitPy.logging.logger import log
from pymongo import MongoClient
from Meolask.meolask import Meolask
from Meolask.modules.service import ServiceRegister
#from Meolask.template import RegisterTemplate
from Meowbot.runtime import *
from Meowbot.services.template_chatgpt import Service as ChatGPTService
from Meowbot.services.template_linebot import Service as LinebotService
#from Meowbot.service import MongoDbCtxType, ServiceType
from Meowbot.services.meowlibot.meowlibot import Agent as LinebotAgent_Meowlibot
from settings import (
    # ChatGPT-turbo
    CHAT_GPT_KEY,
    CHAT_GPT_URL_3,
    CHAT_GPT_MODEL_TURBO,
    # Linebot-Meowlibot
    LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_ACCESS_TOKEN,
    LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_SECRET,
    # Linebot-Ali
    LINE_BOT_AGENT_ALI_CHANNEL_ACCESS_TOKEN,
    LINE_BOT_AGENT_ALI_CHANNEL_SECRET,
)

# 引入：資料庫上下文
from Meowbot.databases.mongodb.user_manager import UserManager
from Meowbot.databases.mongodb.group_manager import GroupManager
# More...

# 引入：控制器
from Meowbot.controllers.linebot_view import linebot_view as LinebotController
# More...

# 服務注冊器(*與控制器、上下文無關聯的獨立服務注冊)
class Services(ServiceRegister):

    # [Abs:Override]：注冊器
    def trigger_registration(self, app: Meolask) -> None:

        self.register(services = [
            ChatGPTService(
                ServiceType.ChatGPT_Turbo,  # Service >> ID
                CHAT_GPT_URL_3,             # ChatGPT >> 連結(API)
                CHAT_GPT_KEY,               # ChatGPT >> 密鑰
                CHAT_GPT_MODEL_TURBO,       # ChatGPT >> 資料模型
            ),
            # More... AI
        ])

        self.register(services = [
            LinebotService(
                ServiceType.LinebotAgent_Meowlibot,                 # Service >> ID
                LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_SECRET,            # Line-bot >> 密鑰
                LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_ACCESS_TOKEN,      # Line-bot >> 訪問令牌(金鑰)
                LinebotAgent_Meowlibot(                             # Agent >> 服務代理：提供服務的對象
                    str(ServiceType.LinebotAgent_Meowlibot.name),   # Agent >> 記錄索引值
                    '_id-gakl94gfdt5ynak6'                          # 代理者ID
                )
            ),
            LinebotService(
                ServiceType.LinebotAgent_Ali,                       # Service >> ID
                LINE_BOT_AGENT_ALI_CHANNEL_SECRET,                  # Line-bot >> 密鑰
                LINE_BOT_AGENT_ALI_CHANNEL_ACCESS_TOKEN,            # Line-bot >> 訪問令牌(金鑰)
                LinebotAgent_Meowlibot(                             # Agent >> 服務代理：提供服務的對象
                    str(ServiceType.LinebotAgent_Ali.name),         # Agent >> 記錄索引值
                    '_id-pnm56asjk45lkakl'                          # 代理者ID
                )
            ),
            # More... LineBot-Agent
        ])


# 資料庫上下文注冊器 (MongoDB)
class MongoDbContexts(ServiceRegister):

    # [Abs:Override]：注冊器
    def trigger_registration(self, app: Meolask, db: MongoClient) -> None:
        pass
        ## 沒有注冊列表，所以不會顯示在 log
        ## MongoDB
        #app.register({
        #    MongoDbCtxType.UserManager: UserManager(db, id=MongoDbCtxType.UserManager),
        #    MongoDbCtxType.GroupManager: GroupManager(db, id=MongoDbCtxType.GroupManager)
        #    # More...
        #})


# 一般控制器注冊
class Controllers(ServiceRegister):

    # [Abs:Override]：注冊器
    def trigger_registration(self, app: Meolask) -> None:
        app.register_view(LinebotController, '/api/linebot', svc_registration_info = self.register(
                services = [
                    LinebotService(
                        ServiceType.LinebotAgent_Meowlibot,                 # Service >> ID
                        LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_SECRET,            # Line-bot >> 密鑰
                        LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_ACCESS_TOKEN,      # Line-bot >> 訪問令牌(金鑰)
                        LinebotAgent_Meowlibot(                             # Agent >> 服務代理：提供服務的對象
                            str(ServiceType.LinebotAgent_Meowlibot.name),   # Agent >> 記錄索引值
                            '_id-gakl94gfdt5ynak6'                          # 代理者ID
                        )
                        # Name = None
                    ),
                    LinebotService(
                        ServiceType.LinebotAgent_Ali,                       # Service >> ID
                        LINE_BOT_AGENT_ALI_CHANNEL_SECRET,                  # Line-bot >> 密鑰
                        LINE_BOT_AGENT_ALI_CHANNEL_ACCESS_TOKEN,            # Line-bot >> 訪問令牌(金鑰)
                        LinebotAgent_Meowlibot(                             # Agent >> 服務代理：提供服務的對象
                            str(ServiceType.LinebotAgent_Ali.name),         # Agent >> 記錄索引值
                            '_id-pnm56asjk45lkakl'                          # 代理者ID
                        )
                        # Name = None
                    ),
                    # More... LineBot-Agent
                ]
            )
        )

