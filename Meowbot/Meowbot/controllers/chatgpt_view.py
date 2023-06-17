'''
提供直接呼叫 GPT
'''
from flask import request, abort
from Meolask.meolask import Meolask
from MeowkitPy.logging.logger import log
from Meowbot.service import ServiceType, MongoDbCtxType
from Meowbot.services.meowlibot import *

def chatgpt_view(app: Meolask, url_prefix: str='/api/chatgpt', services: dict[str,ServiceTemplate]=None):

    # 參數設定
    mode_debug = app.mode_debug

    # 前置檢查：必須要有服務對象的檢查(如無需則注解此段)
    if services == None:
        raise AttributeError(f'Service list cannot be None! >> {__name__}')

    # For 路由
    # -----------------------------------------------------
    '''
    路由： 轉發請求到 ChatGPT API
    '''
    # Meowbot 開放給 外部的 API 入口
    @app.route(url_prefix + '/callback', methods=['POST'])
    def callback():
        # 資料頭(Head)
        check_conditions = '' # 檢查條件
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

            try: # 嘗試執行
                return 'OK'

            except Exception: # 捕獲例外
                abort(400)

        return 'Fail'