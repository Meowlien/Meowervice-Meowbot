from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * # line 所提供的所有 事件

from Meolask.meolask import Meolask
from MeowkitPy.logging.logger import log
from Meowbot.services.meowlibot import * # 所有關於 Meowlibot 事件執行處理器

from settings import (
    LINE_BOT_CHANNEL_ACCESS_TOKEN,
    LINE_BOT_CHANNEL_SECRET
)

def linebot_view(app: Meolask, url_prefix: str='/api/linebot', mode_debug: bool=False):

    # For Debug
    if mode_debug == True:
        log.LogInfomation("Registered >> '" + url_prefix)


    # Line-bot >> 訪問令牌(金鑰)
    line_bot_api = LineBotApi(LINE_BOT_CHANNEL_ACCESS_TOKEN)
    # Line-bot >> 密鑰
    handler = WebhookHandler(LINE_BOT_CHANNEL_SECRET)

    # -----------------------------------------------------

    '''
    路由： 由 Line Developers 中設定的 Webhook URL 來決定 API 路由
    '''
    # Meowbot 開放給 Line 機器人的 API 入口
    @app.route("/callback", methods=['POST'])
    def callback():

        # 資料頭(Head)
        check_conditions = 'X-Line-Signature' # 檢查條件
        is_header_pass, headers = app.check_valid_data(request.headers, check_conditions)
        # 資料體(Body)
        request_data = request.get_data(as_text=True) # as_text = True = Unicode 
        # 跨域資訊(CorsPolicy)
        is_Cors_pass = app.check_has_Cors_Policy()
        # 高速資料庫比對資料(Redis)
        is_redis_pass = app.check_comparison_data()
        # 數據解密(Decryption)
        is_decrypt_pass = app.check_data_decrypt()

        # 是否-通過檢查
        if (is_header_pass == True
            and is_Cors_pass == True
            and is_redis_pass == True
            and is_decrypt_pass == True
        ):
            signature = headers['X-Line-Signature']

            try: # 嘗試執行
                handler.handle(request_data, signature)
                app.logger.info("Request data: " + request_data)

            except InvalidSignatureError: # 捕獲例外
                abort(400)

            return 'OK'

        return 'Fail'




    '''
    Message Event (消息事件)：
    當用戶發送消息時觸發 >> 可以根據不同類型的消息 (文本消息、圖像消息、視頻消息等) 進行相應的處理
    '''
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        msg = event.message.text
        if '測試' in msg:
            #message = imagemap_message()
            #line_bot_api.reply_message(event.reply_token, message)
            pass
        else:
            message = TextSendMessage(text=msg)
            line_bot_api.reply_message(event.reply_token, message)

    '''
    Follow Event (關注事件)：
    當使用者關注您的 Line Bot 時觸發 >> 可以發送歡迎消息或進行其他處理
    '''
    @handler.add(FollowEvent)
    def handle_message(event):
        pass

    '''
    Unfollow Event (取消關注事件)：
    當使用者取消關注您的 Line Bot 時觸發 >> 可以進行相應的清理操作
    '''
    @handler.add(UnfollowEvent)
    def handle_message(event):
        pass

    '''
    Join Event (加入群組/聊天室事件)：
    當 Bot 被邀請加入群組或聊天室時觸發 >> 可以發送歡迎消息或進行其他處理
    '''
    @handler.add(JoinEvent)
    def handle_message(event):
        pass

    '''
    Leave Event (離開群組/聊天室事件)：
    當 Bot 被踢出群組或聊天室時觸發 >> 可以進行相應的清理操作
    '''
    @handler.add(LeaveEvent)
    def handle_message(event):
        pass

    '''
    Member Join Event (成員加入事件)：
    當有新成員加入 Line 群組或聊天室時會觸發該事件 >> 您可以透過此事件來偵測新成員的加入並做出相應的處理
    '''
    @handler.add(MemberJoinedEvent)
    def welcome(event):
        uid = event.joined.members[0].user_id
        gid = event.source.group_id
        profile = line_bot_api.get_group_member_profile(gid, uid)
        name = profile.display_name
        message = TextSendMessage(text=f'{name}歡迎加入')
        line_bot_api.reply_message(event.reply_token, message)

    '''
    Member Left Event (成員離開事件)：
    當有成員離開 Line 群組或聊天室時會觸發該事件 >> 您可以透過此事件來偵測成員的離開並做出相應的處理
    '''
    @handler.add(MemberLeftEvent)
    def handle_message(event):
        pass

    '''
    Postback Event (回傳事件)：
    當使用者在 Line Bot 上進行特定操作 (例如點擊按鈕) 後觸發 >> 可以根據不同的回傳資料進行相應的處理
    '''
    @handler.add(PostbackEvent)
    def handle_message(event):
        print(event.postback.data)

    '''
    Beacon Event (信標事件)：
    當設備附近的信標被檢測到時觸發 >> 可以根據信標的 ID 或 類型 進行相應的處理
    '''
    @handler.add(BeaconEvent)
    def handle_message(event):
        print(event.postback.data)

    '''
    Account Link Event (帳號連結事件)：
    當使用者在 Line Bot 中請求與其外部帳號 (例如:Line Login) 進行關聯時觸發 >> 可以進行帳號關聯的處理
    '''
    @handler.add(AccountLinkEvent)
    def handle_message(event):
        pass

    '''
    Things Event (物聯網事件)：
    與 Line 的物聯網平台連接時觸發的事件 >> 可以與物聯網設備進行互動和控制
    '''
    @handler.add(ThingsEvent)
    def handle_message(event):
        pass

    '''
    [當前版本: 處理器添加變數名稱不確定]
    Flex Message Event (彈性訊息事件)：
    當使用者與彈性訊息互動時觸發 >> 例如點擊按鈕、選擇選項等
    '''

    '''
    [當前版本: 處理器添加變數名稱不確定]
    Location Event (地理位置事件)：
    當使用者分享他們的位置資訊時觸發 >> 可以用於提供相應的位置相關服務
    '''

    '''
    [當前版本: 處理器添加變數名稱不確定]
    Audio Event (音訊事件)：
    當使用者發送音訊訊息時觸發 >> 可以進行相應的音訊處理
    '''

    '''
    [當前版本: 處理器添加變數名稱不確定]
    Video Event (視訊事件)：
    當使用者發送視訊訊息時觸發 >> 可以進行相應的視訊處理
    '''

    '''
    [當前版本: 處理器添加變數名稱不確定]
    Sticker Event (貼圖事件)：
    當使用者發送貼圖訊息時觸發 >> 可以進行相應的貼圖處理
    '''

    '''
    [當前版本: 處理器添加變數名稱不確定]
    File Event (檔案事件)：
    當使用者發送檔案訊息時觸發 >> 可以進行相應的檔案處理
    '''

    '''
    [當前版本: 處理器添加變數名稱不確定]
    Rich Menu Event (豐富選單事件)：
    當使用者與豐富選單互動時觸發 >> 可以根據不同的選單選項進行相應的處理
    '''