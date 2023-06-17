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
