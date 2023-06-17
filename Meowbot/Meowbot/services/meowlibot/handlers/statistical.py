'''
資料統計：統計資料用途
命名規範：以 count_ 作爲前綴
'''
from MeowkitPy.logging.logger import log
from enum import Enum, auto

# 方法列表
# -----------------------------------------------------
class CounterType(Enum):
    GroupMsg = 0
    MemberMsg = auto()
    # More...



# 處理邏輯
# -----------------------------------------------------
# For: 統計群組消息數
def count_group_message():
    pass

# For: 統計用戶於群組的消息數
def count_member_message():
    pass



# 方法清單
# -----------------------------------------------------
def CounterList() -> list:
    return [
        # 務必與<方法列表>所對應的順序相同
        count_group_message(),
        count_member_message(),
        # More...
    ]

