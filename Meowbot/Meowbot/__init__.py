"""
The flask application package.
"""

from Meolask import app


# 引入
from Meowbot.Views.LineBotView import LineBot_View as v_LineBot


# Config
# -----------------------------------------------------
conf_dbgMode = True
# -----------------------------------------------------

# 注冊-路由
app.register_view(v_LineBot,             '/api/lineBot/view', conf_dbgMode)           # 注冊-視圖
