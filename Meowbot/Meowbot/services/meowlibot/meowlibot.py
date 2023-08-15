'''
Meowlibot (阿里機器人)：
事件執行處理器 >> [阿里機器人] 對於 Line 事件觸發後的響應行爲
'''
#from Meowbot.runtime import
from MeowkitPy.data.validation import list_filter
from Meowbot.services.template_linebot import *
from Meowbot.services.meowlibot.handlers.message import instructions as msg_instructions

# Event 事件
# -----------------------------------------------------

# 服務代理對象
class Agent(AgentTemplate):

    _instances: dict[str, AgentTemplate] = {}

    def __init__(self, svc_type: str, id: str='_id-xyz') -> None:
        super().__init__(svc_type, id)
        Agent.__add_instance(id, self)

    # [Override]
    @staticmethod
    def __add_instance(key: str, obj) -> list:
        if isinstance(obj, Agent):
            Agent._instances[key] = obj

    # [Override]
    @staticmethod
    def get_instance(key: str):
        agent: Agent = Agent._instances.get(key, None)
        return agent

    # [Override]：創建執行器
    def build_handlers(self, args: list):

        # 參數檢查
        linebot_api: LineBotApi = list_filter(args, LineBotApi, uniqueness=True)
        if linebot_api is None:
            # 創建 handlers 失敗(原因：沒有創建 handles 時的必要參數)
            log.LogError('Build Handler Fail >> No required parameters >> LinebotApi')
            return

        # 緩存參數
        self.api = linebot_api

        # 創建 handlers
        self.handlers = {
            EventHandler.Message.name:       MessageEventHandler(self.api),
            EventHandler.Follow.name:        FollowEventHandler(self.api),
            EventHandler.UnFollow.name:      UnfollowEventHandler(self.api),
            EventHandler.Join.name:          JoinEventHandler(self.api),
            EventHandler.Leave.name:         LeaveEventHandler(self.api),
            EventHandler.MemberJoin.name:    MemberJoinedEventHandler(self.api),
            EventHandler.MemberLeft.name:    MemberLeftEventHandler(self.api),
            EventHandler.Postback.name:      PostbackEventHandler(self.api),
            EventHandler.Beacon.name:        BeaconEventHandler(self.api),
            EventHandler.AccountLink.name:   AccountLinkEventHandler(self.api),
            EventHandler.Things.name:        ThingsEventHandler(self.api),
        }

# 指令集
class Command(CommandTemplate):

    # 解析指令
    def _parse(self, msg: str, args: dict[str,any]=None) -> tuple[list[str], str]:
        return super()._parse(msg, args) # 沿用：預設解析方法



# Event 事件
# -----------------------------------------------------

class MessageEventHandler(MessageEventHandlerTemplate):

    def __init__(self, api: LineBotApi) -> None:
        super().__init__(api, Command())
        # 指令集注冊
        self.command_register(msg_instructions, args = {
            "TMP":"Temp",
        })

    # [Abs:Override]
    def handle(self, event: MessageEvent):
        self.command.handle(self.linebot_api, event, event.message.text)


class FollowEventHandler(FollowEventHandlerTemplate):
    pass

class UnfollowEventHandler(UnfollowEventHandlerTemplate):
    pass

class JoinEventHandler(JoinEventHandlerTemplate):
    pass

class LeaveEventHandler(LeaveEventHandlerTemplate):
    pass

class MemberJoinedEventHandler(MemberJoinedEventHandlerTemplate):

    # [Abs:Override]
    def handle(self, event: MemberJoinedEvent):
        return
        # 獲取：事件資料
        group_id = event.source.group_id
        user_id = event.source.user_id

        # 獲取：用戶資料(觸發者)
        profile = self.linebot_api.get_profile(user_id)
        display_name = profile.display_name # 用戶-名稱
        picture_url = profile.picture_url   # 用戶-頭像 URL (非公開 = 空字串)

        # Response 響應
        reply_text = msg_welcome(f'{display_name}') # 歡迎致辭
        self.linebot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

class MemberLeftEventHandler(MemberLeftEventHandlerTemplate):
    pass

class PostbackEventHandler(PostbackEventHandlerTemplate):
    pass

class BeaconEventHandler(BeaconEventHandlerTemplate):
    pass

class AccountLinkEventHandler(AccountLinkEventHandlerTemplate):
    pass

class ThingsEventHandler(ThingsEventHandlerTemplate):
    pass

