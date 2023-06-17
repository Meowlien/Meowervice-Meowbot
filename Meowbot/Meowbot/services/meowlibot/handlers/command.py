'''
命令邏輯：接受所有符合規範的命令 & 執行命令
命名規範：以 cmd_ 作爲前綴
'''
from MeowkitPy.logging.logger import log
from enum import Enum, auto

# 方法列表
# -----------------------------------------------------
class CommandType(Enum):
    cmd_executor = 0
    # More...



# 處理邏輯
# -----------------------------------------------------
# For: 解析與執行命令
def cmd_executor():
    pass



# 方法清單
# -----------------------------------------------------
def  CommandList() -> list:
    return [
        # 務必與<方法列表>所對應的順序相同
        cmd_executor(),
        # More...
    ]


