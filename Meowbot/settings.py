import configparser

# config
path_settings = 'settings.ini'
config = configparser.ConfigParser()
config.read(path_settings)
# -------------------------------------------------
HOST = config.get('service', 'host')
PORT = config.get('service', 'port')
LINE_BOT_CHANNEL_ACCESS_TOKEN = config.get('line-bot', 'channel_access_token')
LINE_BOT_CHANNEL_SECRET = config.get('line-bot', 'channel_secret')


#path_others = 'others.ini'
#config = configparser.ConfigParser()
#config.read(path_others)
## -------------------------------------------------
#HOST = config.get('service', 'host')
#PORT = config.get('service', 'port')


