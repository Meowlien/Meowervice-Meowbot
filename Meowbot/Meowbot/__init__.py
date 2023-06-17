import settings as config
from Meolask.meolask import Meolask
from pymongo import MongoClient
from MeowkitPy.logging.logger import log
from Meolask.example.register import ExampleControllers
from Meolask.register import BaseControllers
from Meowbot.register import (
    MongoDbContexts,
    Controllers
)

# 創建：服務項
# -----------------------------------------------------
log.dividers('-')
log.LogInfomation(f'Create Service: Meolask')
app = Meolask(__name__)

log.LogInfomation(f'Create Service: MongoDB >> Connecting...')
mongo_client_ali = MongoClient(config.DB_MONGO_URI_ALI)


# 注冊列表
# -----------------------------------------------------
# 資料庫-注冊表
log.dividers('-')
app.register_database(MongoDbContexts(), mongo_client_ali)
# More...

# 控制器-注冊表
log.dividers('-')
app.register_controllers(BaseControllers())      # 基礎 api (必要)
app.register_controllers(ExampleControllers())   # 範例 api
app.register_controllers(Controllers())          # 自定義 api
# More...


# For: Debug
# -----------------------------------------------------
with app.test_request_context(): # 獲取所有已注冊的路由
    routes = [str(rule) for rule in app.url_map.iter_rules()]
for route in routes: # 輸出所有已注冊的路由
    log.LogInfomation(f'Registered (Route) >> {route}')











# For Test
# -----------------------------------------------------


#try:
#    db: UserManager = app.services['UserManager']
#    db.get_all_users()
#except Exception as e:
#    print(f'Prob >> {e}')




#import requests
#from settings import CHAT_GPT_KEY

#import sys
## 設定 console 編碼為 utf-8
#sys.stdout.reconfigure(encoding='utf-8')

#print(f'Test-Key: {CHAT_GPT_KEY}')
#response = requests.post(
#    'https://api.openai.com/v1/chat/completions',
#    headers={
#        'Content-Type': 'application/json',
#        'Authorization': f'Bearer {CHAT_GPT_KEY}',
#    },
#    json={
#        'model': 'gpt-3.5-turbo',
#        'messages': [
#            {"role": "user", "content": "I'm testing ChatGPT API. U can said anything to prove I'm success."},
#            {"role": "assistant", "content": ""}
#        ],
#    }
#)

#print(response.content.decode('utf-8'))
