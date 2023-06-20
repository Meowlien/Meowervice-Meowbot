'''
消息回復：所有制式回復在此定義
命名規範：以 msg_ 作爲前綴
'''

"""Meowbot.services.meowlibot.handlers.message module."""
from linebot import LineBotApi
from Meowbot.services.meowlibot.handlers.command import *
from MeowkitPy.logging.logger import log
from enum import Enum, auto

# 方法列表
# -----------------------------------------------------
class MessageType(Enum):
    MemberJoin = 0
    MemberLeft = auto()
    # More...



# 處理邏輯
# -----------------------------------------------------
# For: 有人加入群組時
def msg_welcome(user_name: str) -> str:
    print(f'Welcome {user_name}')

# For: 有人離開群組時
def msg_byebye(user_name: str) -> str:
    print(f'Bye Bye for {user_name}')


def callback(command: Command):

    # For: 學你說
    @command.add(cmds=['#imitate'], args=['arg1','arg2'])
    def msg_imitate(linebot_api: LineBotApi, event: MessageEvent, args: list):
        print(f'#imitate Command Test >> {args}')
        return

        # 獲取：事件資料
        user_id = event.source.user_id
        # 獲取：用戶資料(觸發者)
        profile = linebot_api.get_profile(user_id)
        display_name = profile.display_name # 用戶-名稱

        reply_text = f'{display_name} >>\n' + event.message.text
        linebot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

# 方法清單
# -----------------------------------------------------
def  MessageList() -> list:
    return [
        # 務必與<方法列表>所對應的順序相同
        msg_welcome(),
        msg_byebye(),
        # More...
    ]