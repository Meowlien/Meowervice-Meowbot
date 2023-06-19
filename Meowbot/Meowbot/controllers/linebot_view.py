'''
開放給 Line 進行呼叫的 API
'''
from symbol import parameters
from flask import request, abort
from Meolask.meolask import Meolask
from MeowkitPy.logging.logger import log
from MeowkitPy.data.validation import *
from Meowbot.service import ServiceType, MongoDbCtxType
from Meowbot.services.template_linebot import *
from Meowbot.services.template_linebot import Service as LineBotSvc
from Meowbot.databases.mongodb.user_manager import UserManager

from settings import (
    # Meowlibot
    LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_ACCESS_TOKEN,
    LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_SECRET,
)

def linebot_view(app: Meolask, url_prefix: str='/api/linebot', services: dict[str,ServiceTemplate]=None):

    # 參數設定
    # -----------------------------------------------------
    mode_debug = app.mode_debug


    # 前置檢查(注冊時)
    # -----------------------------------------------------
    # 必須要有服務對象的檢查(如無需則注解此段)
    if services == None:
        raise AttributeError(f'Service list cannot be None! >> {__name__}')
    # 1. 至少要有一個 Key 開頭為 ServiceType.LinebotAgent_Xxx 的服務
    svc_linebots: dict[str,LineBotSvc] = dict_filtered(services, 'ServiceType.LinebotAgent_', StringMatchType.StartsWith)
    if len(svc_linebots) == 0:
        raise AttributeError(f'Service[ServiceType.LinebotAgent_???] at least one agent for Linebot! >> {__name__}')


    # For 路由
    # -----------------------------------------------------
    '''
    路由： 由 Line Developers 中設定的 Webhook URL 來決定 API 路由
    '''
    # Meowbot 開放給 Line 機器人的 API 入口
    @app.route(url_prefix + '/callback/<agent_id>', methods=['POST'])
    def callback(agent_id: str):
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
            #channel_secret = request.headers['X-Line-ChannelSecret'] # Undone
            line_signature = headers['X-Line-Signature']
            # 嘗試執行
            try:
                # 事件分發
                if line_signature == 'test':
                    EventHandlerTrigger('message')     # 測試：EventHandlerTrigger 自行分發
                    app.logger.info("Request data: " + request_data)
                else:
                    for svc_linebot in svc_linebots.values():
                        if svc_linebot.agent.agent_id == agent_id:
                            svc_linebot.handler.handle(request_data, line_signature)  # 綫上：WebhookHandler 自動分發
                            app.logger.info("Request data: " + request_data)
                            break
            # 捕獲例外
            except InvalidSignatureError:
                abort(400) # 數位簽章驗證失敗，拒絕請求
                return 'Fail'

        return 'OK'


    # For 事件
    # -----------------------------------------------------

    # 為所有 linebot 服務代理進行方法注冊
    for svc_linebot in svc_linebots.values():
        log.LogInfomation(f'Registered (svc-linebotAgent) >> Agent_id = {svc_linebot.agent.agent_id}')

        #BUG: 第二個會覆蓋第一個

        '''
        Message Event (消息事件)：
        當用戶發送消息時觸發 >> 可以根據不同類型的消息 (文本消息、圖像消息、視頻消息等) 進行相應的處理
        '''
        @svc_linebot.handler.add(MessageEvent, message=TextMessage)
        def on_message_eventHandler(event: MessageEvent):
            print(f'TEST >>>> {svc_linebot.agent.service_type}')
            svc: MessageEventHandlerTemplate = svc_linebot.events[EventHandler.Message.value]
            svc.handle(event)

        '''
        Follow Event (關注事件)：
        當使用者關注您的 Line Bot 時觸發 >> 可以發送歡迎消息或進行其他處理
        '''
        @svc_linebot.handler.add(FollowEvent)
        def on_follow_eventHandler(event: FollowEvent):
            svc = svc_linebot.events[EventHandler.Follow.value]
            svc.handle(event)

        '''
        Unfollow Event (取消關注事件)：
        當使用者取消關注您的 Line Bot 時觸發 >> 可以進行相應的清理操作
        '''
        @svc_linebot.handler.add(UnfollowEvent)
        def on_unfollow_eventHandler(event: UnfollowEvent):
            svc = svc_linebot.events[EventHandler.UnFollow.value]
            svc.handle(event)

        '''
        Join Event (加入群組/聊天室事件)：
        當 Bot 被邀請加入群組或聊天室時觸發 >> 可以發送歡迎消息或進行其他處理
        '''
        @svc_linebot.handler.add(JoinEvent)
        def on_join_eventHandler(event: JoinEvent):
            svc = svc_linebot.events[EventHandler.Join.value]
            svc.handle(event)

        '''
        Leave Event (離開群組/聊天室事件)：
        當 Bot 被踢出群組或聊天室時觸發 >> 可以進行相應的清理操作
        '''
        @svc_linebot.handler.add(LeaveEvent)
        def on_leave_eventHandler(event: LeaveEvent):
            svc = svc_linebot.events[EventHandler.Leave.value]
            svc.handle(event)

        '''
        Member Join Event (成員加入事件)：
        當有新成員加入 Line 群組或聊天室時會觸發該事件 >> 您可以透過此事件來偵測新成員的加入並做出相應的處理
        '''
        @svc_linebot.handler.add(MemberJoinedEvent)
        def on_welcome_eventHandler(event: MemberJoinedEvent):
            svc = svc_linebot.events[EventHandler.MemberJoin.value]
            svc.handle(event)

        '''
        Member Left Event (成員離開事件)：
        當有成員離開 Line 群組或聊天室時會觸發該事件 >> 您可以透過此事件來偵測成員的離開並做出相應的處理
        '''
        @svc_linebot.handler.add(MemberLeftEvent)
        def on_byebye_eventHandler(event: MemberLeftEvent):
            svc = svc_linebot.events[EventHandler.MemberLeft.value]
            svc.handle(event)

        '''
        Postback Event (回傳事件)：
        當使用者在 Line Bot 上進行特定操作 (例如點擊按鈕) 後觸發 >> 可以根據不同的回傳資料進行相應的處理
        '''
        @svc_linebot.handler.add(PostbackEvent)
        def on_postback_eventHandler(event: PostbackEvent):
            svc = svc_linebot.events[EventHandler.Postback.value]
            svc.handle(event)

        '''
        Beacon Event (信標事件)：
        當設備附近的信標被檢測到時觸發 >> 可以根據信標的 ID 或 類型 進行相應的處理
        '''
        @svc_linebot.handler.add(BeaconEvent)
        def on_beacon_eventHandler(event: BeaconEvent):
            svc = svc_linebot.events[EventHandler.Beacon.value]
            svc.handle(event)

        '''
        Account Link Event (帳號連結事件)：
        當使用者在 Line Bot 中請求與其外部帳號 (例如:Line Login) 進行關聯時觸發 >> 可以進行帳號關聯的處理
        '''
        @svc_linebot.handler.add(AccountLinkEvent)
        def on_accountLink_eventHandler(event: AccountLinkEvent):
            svc = svc_linebot.events[EventHandler.AccountLink.value]
            svc.handle(event)

        '''
        Things Event (物聯網事件)：
        與 Line 的物聯網平台連接時觸發的事件 >> 可以與物聯網設備進行互動和控制
        '''
        @svc_linebot.handler.add(ThingsEvent)
        def on_things_eventHandler(event: ThingsEvent):
            svc = svc_linebot.events[EventHandler.Things.value]
            svc.handle(event)

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

    log.dividers()

    # For Test
    def EventHandlerTrigger(event_type: str):
        if event_type == 'message':             on_message_eventHandler('test')
        elif event_type == 'follow':            on_follow_eventHandler('test')
        elif event_type == 'unfollow':          on_unfollow_eventHandler('test')
        elif event_type == 'join':              on_join_eventHandler('test')
        elif event_type == 'leave':             on_leave_eventHandler('test')
        elif event_type == 'postback':          on_postback_eventHandler('test')
        elif event_type == 'beacon':            on_beacon_eventHandler('test')
        elif event_type == 'accountLink':       on_accountLink_eventHandler('test')
        elif event_type == 'memberJoined':      on_welcome_eventHandler('test')
        elif event_type == 'memberLeft':        on_byebye_eventHandler('test')
        elif event_type == 'things':            on_things_eventHandler('test')
        elif event_type == 'unsend':            pass
        elif event_type == 'videoPlayComplete': pass
        else: log.LogInfomation('Unknown event type. type=' + event_type)

