'''
消息回復：所有制式回復在此定義
命名規範：以 msg_ 作爲前綴
'''
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



# 方法清單
# -----------------------------------------------------
def  MessageList() -> list:
    return [
        # 務必與<方法列表>所對應的順序相同
        msg_welcome(),
        msg_byebye(),
        # More...
    ]