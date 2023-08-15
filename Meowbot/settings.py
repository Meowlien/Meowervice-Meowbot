import configparser
from MeowkitPy.logging.logger import log

# config
path_settings = 'settings.ini'
config = configparser.ConfigParser()

try:
    config.read(path_settings, encoding='utf-8')

    # service
    # -------------------------------------------------
    HOST = config.get('service', 'host')
    PORT = config.get('service', 'port')

    # mongodb
    # -------------------------------------------------
    DB_MONGO_HOST = config.get('mongodb', 'host')
    DB_MONGO_PORT = config.get('mongodb', 'port')
    DB_MONGO_CONNECT_STR = f'mongodb://{DB_MONGO_HOST}:{DB_MONGO_PORT}/'
    DB_MONGO_URI_ALI_ID = config.get('mongodb', 'uri_ali_id')
    DB_MONGO_URI_ALI_PWD = config.get('mongodb', 'uri_ali_pwd')
    DB_MONGO_URI_ALI_CLUSTER = config.get('mongodb', 'uri_ali_cluster')
    DB_MONGO_URI_ALI = f'mongodb+srv://{DB_MONGO_URI_ALI_ID}:{DB_MONGO_URI_ALI_PWD}@{DB_MONGO_URI_ALI_CLUSTER}.mongodb.net/'
    DB_MONGO_URI_ALI_PROTECT = f'mongodb+srv://{DB_MONGO_URI_ALI_ID}:****@{DB_MONGO_URI_ALI_CLUSTER}.mongodb.net/'

    # line-bot
    # -------------------------------------------------
    # Meowlibot
    LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_ACCESS_TOKEN = config.get('line-bot', 'agent_meowlibot_token')
    LINE_BOT_AGENT_MEOWLIBOT_CHANNEL_SECRET = config.get('line-bot', 'agent_meowlibot_secret')
    # Ali
    LINE_BOT_AGENT_ALI_CHANNEL_ACCESS_TOKEN = config.get('line-bot', 'agent_ali_token')
    LINE_BOT_AGENT_ALI_CHANNEL_SECRET = config.get('line-bot', 'agent_ali_secret')

    # ChatGPT
    # -------------------------------------------------
    CHAT_GPT_KEY = config.get('chatgpt', 'key')
    # [chatgpt.endpoint_url]
    CHAT_GPT_URL_PG = config.get('chatgpt.endpoint_url', 'OpenAi_Playground')
    CHAT_GPT_URL_3 = config.get('chatgpt.endpoint_url', 'OpenAi_GPT-3')
    CHAT_GPT_URL_4 = config.get('chatgpt.endpoint_url', 'OpenAi_GPT-4')
    # [chatgpt.model]
    CHAT_GPT_MODEL_TURBO = config.get('chatgpt.model', 'GPT_turbo')
    CHAT_GPT_MODEL_DAVINCI_2 = config.get('chatgpt.model', 'GPT_davinci-2')
    CHAT_GPT_MODEL_DAVINCI_3 = config.get('chatgpt.model', 'GPT_davinci-3')

# 捕獲例外：當找不到指定參數欄位時
except configparser.NoSectionError:
    raise Exception(f'\n>>>> Setting.py: Get Section Fail. section does not exist.\n')
except configparser.NoOptionError:
    raise Exception(f'\n>>>> Setting.py: Get Option Fail. option does not exist.\n')