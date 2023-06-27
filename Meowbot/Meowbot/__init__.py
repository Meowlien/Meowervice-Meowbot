import settings as config
from Meolask.meolask import Meolask
from pymongo import MongoClient
from MeowkitPy.logging.logger import log
from Meolask.example.register import ExampleControllers
from Meolask.register import BaseControllers
from Meolask.template import RegisterTemplate
from Meowbot.service import Container
from Meowbot.register import (
    show_registry,
    Services,
    MongoDbContexts,
    Controllers
)

# 初始化設定
# -----------------------------------------------------
RegisterTemplate.initialize(Container.services)
RegisterTemplate.debug_compare_registry(Container.services)


# 創建：服務項
# -----------------------------------------------------
log.dividers('-')
log.LogInfomation(f'Create Service: Meolask')
app = Meolask(__name__)

log.LogInfomation(f'Create Service: MongoDB >> Connecting...')
mongo_client_ali = MongoClient(config.DB_MONGO_URI_ALI)
log.dividers('-')

# 注冊列表(每個注冊都以組為單位，即一個注冊内容中，有許多注冊項)
# -----------------------------------------------------

# 服務-注冊表
app.register_services(Services())   # 服務項
# More...

# 資料庫-注冊表
app.register_database(MongoDbContexts(), mongo_client_ali) # BUG: 第二個參數形態不符
# More...

# 控制器-注冊表
app.register_controllers(BaseControllers())      # 基礎 api (必要)
app.register_controllers(ExampleControllers())   # 範例 api
app.register_controllers(Controllers())          # 自定義 api
# More...


# For Debug
if app.mode_debug == True:

    # 顯示 <服務-注冊表> 清單
    show_registry()
    log.dividers('-')

    # 顯示 <資料庫上下文-注冊表> 清單
    # todo:
    #log.dividers('-')

    # 顯示 <控制器-注冊表> 清單
    with app.test_request_context(): # 獲取所有已注冊的路由
        routes = [str(rule) for rule in app.url_map.iter_rules()]
    for route in routes: # 輸出所有已注冊的路由
        log.LogInfomation(f'Registered (Route) >> {route}')
    log.dividers('-')


    # DEBUG >> 驗證
    #RegisterTemplate.debug_compare_registry(Container.services)
