from Meolask.meolask import Meolask
from Meolask.register import ControllerRegister

# 創建 app 實體
app = Meolask(__name__)

# Config
# -----------------------------------------------------
mode_debug: bool = True
# -----------------------------------------------------

# 準備：控制器注冊表單
controllers = ControllerRegister(app, mode_debug)

# 注冊：控制器
app.register_controller(controllers)



# For Test
# -----------------------------------------------------

