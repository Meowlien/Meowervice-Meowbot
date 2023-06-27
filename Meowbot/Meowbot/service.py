﻿'''
服務清單：為避免多個 Service 在注冊到 Controller 時，造成 key 衝突
'''
from abc import ABC, abstractmethod
from enum import Enum, auto

# 容器: 全域
class Container(ABC):
    services: dict['ServiceType', any] = None


# 上下文
class MongoDbCtxType(Enum):
    UserManager = 0,
    GroupManager = auto()

# 服務項
class ServiceType(Enum):
    # Linebot 服務請遵循命名規範： LinebotAgent_Xxx
    LinebotAgent_Meowlibot = 0,
    LinebotAgent_Ali = auto(),
    # ChatGPT
    ChatGPT_Turbo = auto(),

