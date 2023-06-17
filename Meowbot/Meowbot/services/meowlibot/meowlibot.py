'''
Meowlibot (阿里機器人)：
事件執行處理器 >> [阿里機器人] 對於 Line 事件觸發後的響應行爲
'''
from Meowbot.services.template_linebot import *
from Meowbot.services.meowlibot.handlers.message import *

'''
Message Event (消息事件)：
當用戶發送消息時觸發 >> 可以根據不同類型的消息 (文本消息、圖像消息、視頻消息等) 進行相應的處理
'''
class MessageEventHandler(MessageEventHandlerTemplate):

    # [Abs:Override]
    def handle(self, event: MessageEvent):

        # For 私聊時
        if event.source.type == 'user':
            pass

        # For 群聊時
        if event.source.type == 'group':
            pass

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

# Service
def meowlibot(api: LineBotApi) -> list:
    return [
        # 請參照 EventHandler 的順序
        MessageEventHandler(api),
        FollowEventHandler(api),
        UnfollowEventHandler(api),
        JoinEventHandler(api),
        LeaveEventHandler(api),
        MemberJoinedEventHandler(api),
        MemberLeftEventHandler(api),
        PostbackEventHandler(api),
        BeaconEventHandler(api),
        AccountLinkEventHandler(api),
        ThingsEventHandler(api)
        # More...
    ]
