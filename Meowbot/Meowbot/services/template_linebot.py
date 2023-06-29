'''
Bot (機器人)：
事件執行處理器 >> [機器人] 對於 Line 事件觸發後的響應行爲
以下均為 [機器人] 抽象類 作爲界面 (interface)
'''

from abc import ABC, abstractmethod
from Meolask.modules.service import ServiceTemplate
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * # line 所提供的所有 事件定義
from MeowkitPy.logging.logger import log
from enum import Enum, auto
import functools
import typing

# Linebot 服務 >> 注冊時創建
class Service(ServiceTemplate):

    # 建構式
    def __init__(self, id: str, channel_secret: str, channel_access_token: str, agent: 'AgentTemplate', name: str=None) -> None:
        super().__init__(id, name)
        self.channel_secret = channel_secret                    # Line-bot >> 密鑰
        self.channel_access_token = channel_access_token        # Line-bot >> 訪問令牌(金鑰)
        self.agent = agent                                      # Agent >> 服務代理對象(Line機器人的靈魂)
        try: # 嘗試執行
            self.handler = WebhookHandler(self.channel_secret)  # Webhook 處理器(事件分配器)
            self.api = LineBotApi(self.channel_access_token)    # Line-Api >> 程式界面/接口
            self.agent.build_handlers(args=[self.api])          # Line-bot >> 事件處理器
            #self.handlers = self.agent.build_handlers(args=[self.api]) # Line-bot >> 事件處理器
        except Exception as e: # 發生例外
            log.LogError(f'Create Linebot Service Fail! >> {e}')
    
    # 為執行器添加參數
    def handler_add_svc_linebot(self, args: list=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(event):
                return func(event, self, args)
            return wrapper
        return decorator

# Linebot 服務代理模板 >> 注冊 Linebot 服務時，可使用相同代理者不同實例 (以實現彈性切換機器人服務)
class AgentTemplate(ABC):

    def __init__(self, svc_type: str, id: str='_id-xyz') -> None:
        self.service_type = svc_type                    # 代理對象(可以看作是名稱，但同一個名稱可能有很多個實例)
        self.id = id                                    # 對象實例(同一個代理模型，不同實例下的id)
        self.agent_id = self.service_type + self.id     # 代理對象唯一識別符
        self.handlers: dict = None                      # 執行器

    # [virtual]: 緩存代理實例
    @staticmethod # 靜態函式
    def __add_instance(key: str, obj) -> list:
        pass

    # [virtual]: 獲取代理實例
    @staticmethod # 靜態函式
    def get_instance(key: str):
        pass

    @abstractmethod # 構建執行器清單
    def build_handlers(self, args: list):
        pass

    # 獲取執行器
    def get_handler(self, key: str):
        return self.handlers.get(key, None)

# 指令注冊器模板
class CommandTemplate(ABC):

    def __init__(self) -> None:
        self._handlers = {}     # 指令執行器
        self._default = None    # 預設執行器

    # 注冊
    def add(self, cmds: list[str], args: dict[str,any]=None):
        def decorator(func):
            for cmd in cmds:

                # 解析指令格式
                _, result = self._parse(cmd, args={'sliced':'False'})
                if _ is None:
                    log.LogWarning(f'(When call register) {result}')
                    return

                # 注冊執行器
                self._handlers[cmd] = (func, args)
                
            return func

        return decorator

    # 執行器
    def handle(self, linebot_api: LineBotApi, event: any, cmd: str=None):

        # 1. 分析 event 中的指令
        tokens, result = self._parse(cmd)
        if tokens == None:
            log.LogWarning(f'(When call handle): {result}')
            return

        # 2. 根據指令 調用對應方法
        key = tokens[0]
        (func, args) = self._handlers.get(key, (None, None))

        # 切換成預設執行器
        if func is None:
            func = self._default

        # 最後檢查
        if func is None:
            print('No handler of ' + 'command' + ' and no default handler')
        else:
            args['tokens'] = tokens
            self.__invoke_func(func, linebot_api, event, args)

    # 執行
    def __invoke_func(self, func, linebot_api: LineBotApi, event: 'EventHandlerTemplate', args: dict[str,any]=None):
        if args != None:
            func(linebot_api, event, args)
        else:
            func(linebot_api, event, None)

    @abstractmethod # 解析指令
    def _parse(self, msg: str, args: dict[str,any]=None) -> tuple[list[str], str]:
        pass
        #'''
        #説明：以下僅供參考
        #parse(self, msg: str, sliced: bool=True)
        #-----------------------------------------------------
        #'''

        ## 參數設定
        #arg_sliced: bool = True
        #if args is not None:
        #    arg_sliced = args.get('sliced', False)

        ## 長度不符最低解析標準 >> 3位字元
        #if len(msg) <= 2:
        #    return None, f'Command Parse Fail! >> At least 3 length >> {msg}'

        ## 指令的第一個字元必須爲 #
        #if msg[0] != '#':
        #    return None, f'Command Parse Fail! >> First char should be # >> {msg}'

        ## 是否將語句切片
        #if arg_sliced == True:
        #    # 指令判定失敗(不是指令 or 語法錯誤)
        #    tokens = msg.split() # 以空格分割
        #    if len(tokens) == 1:
        #        return None, f'Command Parse Fail! >> Syntax Error >> {msg}'

        #    # 切片處理
        #    return tokens, 'pass'

        ## 維持(以表示解析 即便不切片 也通過)
        #return msg, 'pass'
        #'''
        #-----------------------------------------------------
        #'''
        pass


# 事件執行器
# -----------------------------------------------------

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

    def __init__(self, api: LineBotApi, command: CommandTemplate=None) -> None:
        self.linebot_api = api
        self.command = command

    # 指令注冊
    def command_register(self, func:any, args: dict[str,any]=None):
        try:
            func(self.command, args)
        except AttributeError as e:
            log.LogWarning(f'Command Register Fail >> {e}')

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
