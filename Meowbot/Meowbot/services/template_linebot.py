'''
Bot (機器人)：
事件執行處理器 >> [機器人] 對於 Line 事件觸發後的響應行爲
以下均為 [機器人] 抽象類 作爲界面 (interface)
'''
from Meolask.template import ServiceTemplate
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * # line 所提供的所有 事件定義
from MeowkitPy.logging.logger import log
from enum import Enum, auto

# Linebot 服務代理模板 >> 注冊 Linebot 服務時，可同代理者 (以實現彈性切換機器人服務)
class AgentTemplate():

    def __init__(self, svc_type: str, id: str='_id-xyz') -> None:
        self.service_type = svc_type
        self.id = id
        self.agent_id = self.service_type + self.id

    # [abstruct]
    def handlers(self, api: LineBotApi) -> list:
        pass

# Linebot 服務 >> 注冊時創建
class Service(ServiceTemplate):
    def __init__(self, channel_secret: str, channel_access_token: str, agent: AgentTemplate, name: str=None) -> None:
        super().__init__(name)
        self.channel_secret = channel_secret                    # Line-bot >> 密鑰
        self.channel_access_token = channel_access_token        # Line-bot >> 訪問令牌(金鑰)
        self.agent = agent                                      # Agent >> 服務代理對象(Line機器人的靈魂)
        try: # 嘗試執行
            self.handler = WebhookHandler(self.channel_secret)  # Webhook 處理器
            self.api = LineBotApi(self.channel_access_token)    # Line-Api >> 程式界面/接口
            self.events = self.agent.handlers(self.api)         # Line-bot >> 事件處理器
        except Exception as e: # 發生例外
            log.LogError(f'Create Linebot Service Fail! >> {e}')

# 事件執行器 清單
class EventHandler(Enum):
    Message = 0
    Follow = auto()
    UnFollow = auto()
    Join = auto()
    Leave = auto()
    MemberJoin = auto()
    MemberLeft = auto()
    Postback = auto()
    Beacon = auto()
    AccountLink = auto()
    Things = auto()

# 事件執行器 模板
class EventHandlerTemplate():

    def __init__(self, api: LineBotApi) -> None:
        self.linebot_api = api

    # [abstruct]
    def handle(self, event: any):
        print(f'EventHandlerTemplate')
        pass

# 事件執行器
# -----------------------------------------------------

class MessageEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: MessageEvent):
        super().handle(event)
        pass

class FollowEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: FollowEvent):
        super().handle(event)
        pass

class UnfollowEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: UnfollowEvent):
        super().handle(event)
        pass

class JoinEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: JoinEvent):
        super().handle(event)
        pass

class LeaveEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: LeaveEvent):
        super().handle(event)
        pass

class MemberJoinedEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: MemberJoinedEvent):
        super().handle(event)
        pass

class MemberLeftEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: MemberLeftEvent):
        super().handle(event)
        pass

class PostbackEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: PostbackEvent):
        super().handle(event)
        pass

class BeaconEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: BeaconEvent):
        super().handle(event)
        pass

class AccountLinkEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: AccountLinkEvent):
        super().handle(event)
        pass

class ThingsEventHandlerTemplate(EventHandlerTemplate):
    # [abstruct]
    def handle(self, event: ThingsEvent):
        super().handle(event)
        pass
