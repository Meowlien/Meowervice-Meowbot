﻿from Meolask import Meolask
from Meolask.Logging.Logger import Log
from flask import request, abort
from datetime import datetime

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import configparser

def LineBot_View(app: Meolask, url_prefix: str='/api/view', dbgInfo: bool=False):

    # 設定檔
    config = configparser.ConfigParser()
    config.read('settings.ini') # 讀取-設定檔
    #config.get('欄位', '變數名稱')

    # Channel Access Token
    line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
    # Channel Secret
    handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

    if dbgInfo == True:
        Log.LogInfomation("Registered >> '" + url_prefix)




    # 監聽所有來自 /callback 的 Post Request
    @app.route("/callback", methods=['POST'])
    def callback():
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']
        # get request body as text
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return 'OK'

    # 處理訊息
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        msg = event.message.text

        if '最新合作廠商' in msg:
            message = imagemap_message()
            line_bot_api.reply_message(event.reply_token, message)
        elif '最新活動訊息' in msg:
            message = buttons_message()
            line_bot_api.reply_message(event.reply_token, message)
        elif '註冊會員' in msg:
            message = Confirm_Template()
            line_bot_api.reply_message(event.reply_token, message)
        elif '旋轉木馬' in msg:
            message = Carousel_Template()
            line_bot_api.reply_message(event.reply_token, message)
        elif '圖片畫廊' in msg:
            message = Image_CarouselTemplate()
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text=msg)
            line_bot_api.reply_message(event.reply_token, message)

    # 按鈕 or 模板 元素觸發時
    @handler.add(PostbackEvent)
    def handle_message(event):
        print(event.postback.data)

    # 成員加入群組時
    @handler.add(MemberJoinedEvent)
    def welcome(event):
        uid = event.joined.members[0].user_id
        gid = event.source.group_id
        profile = line_bot_api.get_group_member_profile(gid, uid)
        name = profile.display_name
        message = TextSendMessage(text=f'{name}歡迎加入')
        line_bot_api.reply_message(event.reply_token, message)
