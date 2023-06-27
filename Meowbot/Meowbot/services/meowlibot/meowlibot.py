'''
Meowlibot (阿里機器人)：
事件執行處理器 >> [阿里機器人] 對於 Line 事件觸發後的響應行爲
'''
from Meowbot.service import ServiceType
from MeowkitPy.data.validation import list_filter
from Meowbot.services.template_linebot import *
from Meowbot.services.meowlibot.handlers.message import instructions as msg_instructions


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

    # [abstruct]: 解析指令
    '''
    param: args >> sliced:bool
    '''
    def _parse(self, msg: str, args: dict[str,any]=None) -> tuple[list[str], str]:

        # 參數設定
        arg_sliced: bool = True
        if args is not None:
            arg_sliced = args.get('sliced', False)

        # 長度不符最低解析標準 >> 3位字元
        if len(msg) <= 2:
            return None, f'Command Parse Fail! >> At least 3 length >> {msg}'

        # 指令的第一個字元必須爲 #
        if msg[0] != '#':
            return None, f'Command Parse Fail! >> First char should be # >> {msg}'

        # 是否將語句切片
        if arg_sliced == True:
            # 指令判定失敗(不是指令 or 語法錯誤)
            tokens = msg.split() # 以空格分割
            if len(tokens) == 1:
                return None, f'Command Parse Fail! >> Syntax Error >> {msg}'

            # 切片處理
            return tokens, 'pass'

        # 維持(以表示解析 即便不切片 也通過)
        return msg, 'pass'

'''
Message Event (消息事件)：
當用戶發送消息時觸發 >> 可以根據不同類型的消息 (文本消息、圖像消息、視頻消息等) 進行相應的處理
'''
class MessageEventHandler(MessageEventHandlerTemplate):

    def __init__(self, api: LineBotApi) -> None:
        super().__init__(api, Command())
        # 指令集注冊
        self.command_register(msg_instructions)


    # [Abs:Override]
    def handle(self, event: MessageEvent):
        self.command.handle(self.linebot_api, event, event.message.text)

        ## 獲取：事件資料
        ##group_id = event.source.group_id
        #user_id = event.source.user_id

        ## 獲取：用戶資料(觸發者)
        #profile = self.linebot_api.get_profile(user_id)
        #display_name = profile.display_name # 用戶-名稱
        #picture_url = profile.picture_url   # 用戶-頭像 URL (非公開 = 空字串)


        #msg = event.message.text
        #print(f'Get: MessageEventHandler >> {msg}')

        #if len(msg) > 0 and msg[0] == '#':
        #    reply_text = f'{display_name} >>\n' + event.message.text
        #    self.linebot_api.reply_message(
        #        event.reply_token,
        #        TextSendMessage(text=reply_text)
        #    )

        #event.message
        ## For 私聊時
        #if event.source.type == 'user':
        #    pass

        ## For 群聊時
        #if event.source.type == 'group':
        #    pass

        pass

'''
Follow Event (關注事件)：
當使用者關注您的 Line Bot 時觸發 >> 可以發送歡迎消息或進行其他處理
'''
class FollowEventHandler(FollowEventHandlerTemplate):
    pass

'''
Unfollow Event (取消關注事件)：
當使用者取消關注您的 Line Bot 時觸發 >> 可以進行相應的清理操作
'''
class UnfollowEventHandler(UnfollowEventHandlerTemplate):
    pass

'''
Join Event (加入群組/聊天室事件)：
當 Bot 被邀請加入群組或聊天室時觸發 >> 可以發送歡迎消息或進行其他處理
'''
class JoinEventHandler(JoinEventHandlerTemplate):
    pass

'''
Leave Event (離開群組/聊天室事件)：
當 Bot 被踢出群組或聊天室時觸發 >> 可以進行相應的清理操作
'''
class LeaveEventHandler(LeaveEventHandlerTemplate):
    pass

'''
Member Join Event (成員加入事件)：
當有新成員加入 Line 群組或聊天室時會觸發該事件 >> 您可以透過此事件來偵測新成員的加入並做出相應的處理
'''
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

'''
Member Left Event (成員離開事件)：
當有成員離開 Line 群組或聊天室時會觸發該事件 >> 您可以透過此事件來偵測成員的離開並做出相應的處理
'''
class MemberLeftEventHandler(MemberLeftEventHandlerTemplate):
    pass

'''
Postback Event (回傳事件)：
當使用者在 Line Bot 上進行特定操作 (例如點擊按鈕) 後觸發 >> 可以根據不同的回傳資料進行相應的處理
'''
class PostbackEventHandler(PostbackEventHandlerTemplate):
    pass

'''
Beacon Event (信標事件)：
當設備附近的信標被檢測到時觸發 >> 可以根據信標的 ID 或 類型 進行相應的處理
'''
class BeaconEventHandler(BeaconEventHandlerTemplate):
    pass

'''
Account Link Event (帳號連結事件)：
當使用者在 Line Bot 中請求與其外部帳號 (例如:Line Login) 進行關聯時觸發 >> 可以進行帳號關聯的處理
'''
class AccountLinkEventHandler(AccountLinkEventHandlerTemplate):
    pass

'''
Things Event (物聯網事件)：
與 Line 的物聯網平台連接時觸發的事件 >> 可以與物聯網設備進行互動和控制
'''
class ThingsEventHandler(ThingsEventHandlerTemplate):
    pass

