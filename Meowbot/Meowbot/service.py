from enum import Enum, auto

# 上下文
class MongoDbCtxType(Enum):
    UserManager = 0
    GroupManager = auto()

# 服務項
class ServiceType(Enum):
    LinebotService = 0


