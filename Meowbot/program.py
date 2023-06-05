# from Program
"""
This script runs the BotService application using a development server.
"""
import configparser
from Meolask import app
import Meowbot

# 設定檔
config = configparser.ConfigParser()
config.read('settings.ini') # 讀取-設定檔
#config.get('欄位', '變數名稱')

# 主程式
if __name__ == '__main__':

    HOST = config.get('Service', 'Host')
    PORT = config.get('Service', 'Port')

    app.run(HOST, PORT)



## Tmp
#from os import environ
#HOST = environ.get('SERVER_HOST', 'localhost')
#PORT = environ.get('SERVER_PORT', '5555')
