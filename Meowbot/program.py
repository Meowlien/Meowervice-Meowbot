import sys
import os

# 获取当前文件的路径
current_dir = os.path.dirname(__file__)

# 获取外部项目的路径
meolask_path = os.path.join(current_dir, '..', '..', 'MeowlatePy-Meolask', 'Meolask')
meowkitpy_path = os.path.join(current_dir, '..', '..', 'MeowkitPy', 'MeowkitPy')

# 将外部项目路径添加到 sys.path 中
sys.path.append(meolask_path)
sys.path.append(meowkitpy_path)


from pymongo.errors import ServerSelectionTimeoutError
from MeowkitPy.logging.logger import log
import settings as config

# 主程式
from Meowbot import app, mongo_client_ali
if __name__ == '__main__':

    # 資料庫
    try:
        mongo_client_ali.server_info() # 執行一個查詢以確認連線
        log.LogInfomation(f'**************************************')
        log.LogInfomation(f'MongoDb is connected on >> {config.DB_MONGO_URI_ALI_PROTECT}')
        log.LogInfomation(f'**************************************')

    except ServerSelectionTimeoutError:
        log.LogInfomation(f'**************************************')
        log.LogWarning('MongoDb connect Fail')
        log.LogInfomation(f'**************************************')


    HOST = config.HOST
    PORT = config.PORT
    app.run(HOST, PORT)
