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

class Service(ServiceTemplate):
    def __init__(self, channel_secret: str, channel_access_token: str, handlers: list,
        name: str=None) -> None:
        super().__init__(name)
        try:
            self.handler = WebhookHandler(channel_secret)  # Line-bot >> 密鑰
            self.api = LineBotApi(channel_access_token)    # Line-bot >> 訪問令牌(金鑰)
            self.events = handlers(self.api)                  # 提供服務的對象
        except Exception as e:
            log.LogError(f'Linebot Fail! >> {e}')

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

class EventHandlerTemplate():

    def __init__(self, api: LineBotApi) -> None:
        self.linebot_api = api

    # [abstruct]
    def handle(self, event: any):
        print(f'EventHandlerTemplate')
        pass

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
