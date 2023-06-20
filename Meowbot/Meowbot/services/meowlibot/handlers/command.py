
"""Meowbot.services.meowlibot.handlers.command module."""

from linebot import LineBotApi
from linebot.models import *
from MeowkitPy.logging.logger import log

class Command():

    def __init__(self) -> None:
        self._handlers = {}     # 指令執行器
        self._default = None    # 預設執行器

    # 注冊器
    def add(self, cmds: list[str], args: list=None):
        def decorator(func):

            for cmd in cmds:

                # 解析指令格式
                if self.parse(cmd, False, 'Register') is None:
                    # 指令格式錯誤
                    return

                self._handlers[cmd] = (func, args) # 注冊執行器

            return func

        return decorator

    # 執行器
    def handle(self, linebot_api:LineBotApi, event):

        # 1. 分析 event 中的指令
        msg:str = event if isinstance(event, str) else event.message.text
        tokens = self.parse(msg, caller='Command.handle()')
        if tokens == None:
            # 指令格式錯誤
            return

        # 2. 根據指令 調用對應方法
        key = tokens[0]
        (func, args) = self._handlers.get(key, (None, None))

        
        if func is None:
            func = self._default # 切換成預設執行器

        # 最後檢查
        if func is None:
            print('No handler of ' + 'command' + ' and no default handler')
        else:
            self.__invoke_func(func, linebot_api, event, args)

    # 執行
    def __invoke_func(self, func, linebot_api, event, args):
        if args != None:
            func(linebot_api, event, args)
        else:
            func(linebot_api, event, None)

    # For: 解析指令 (指令規則)
    def parse(self, msg: str, sliced: bool=True, caller: str='Function') -> list[str]:

        # 長度不符最低解析標準 >> 3位字元
        if len(msg) <= 2:
            print(f'({caller}) Command Parse Fail! >> At least 3 length >> {msg}')
            return None

        # 指令的第一個字元必須爲 #
        if msg[0] != '#':
            print(f'({caller}) Command Parse Fail! >> First char should be # >> {msg}')
            return None

        # 是否將語句切片
        if sliced == True:
            # 指令判定失敗(不是指令 or 語法錯誤)
            tokens = msg.split() # 以空格分割
            if len(tokens) == 1:
                print(f'Command Parse Fail! >> Syntax Error >> {msg}')
                return None

            # 切片處理
            return tokens

        # 維持(以表示解析通過)
        return msg


