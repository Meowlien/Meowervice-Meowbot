from abc import ABC, abstractmethod
from enum import Enum, auto
from Meolask.modules.service import ServiceTemplate
from MeowkitPy.logging.logger import log

class Runtime(ABC):
    # 注冊表：服務項
    registry_service: dict['ServiceType', ServiceTemplate] = None

    @staticmethod
    def show_reg_service_info():
        for key, val in Runtime.registry_service.items():
            log.LogInfomation(f'Registered (Service) >> {val.id}')


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