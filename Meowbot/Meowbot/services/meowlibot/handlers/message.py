"""Meowbot.services.meowlibot.handlers.message module."""

'''
消息回復：所有制式回復在此定義
命名規範：以 msg_ 作爲前綴
'''
from linebot import LineBotApi
from linebot.models import * # line 所提供的所有 事件定義
from Meowbot.services.template_linebot import CommandTemplate
from MeowkitPy.logging.logger import log

# 指令集
def instructions(command: CommandTemplate):
    #log.LogInfomation(f'Registered >> Message Instructions Set')


    ## For: 有人加入群組時
    #def msg_welcome(user_name: str) -> str:
    #    print(f'Welcome {user_name}')

    ## For: 有人離開群組時
    #def msg_byebye(user_name: str) -> str:
    #    print(f'Bye Bye for {user_name}')


    # For: 學你說
    @command.add(cmds=['###'], args={'tokens':None})
    def msg_imitate(linebot_api: LineBotApi, event, args: dict[str,any]):

        tokens = args.get('tokens', ['#fail','[Warnning]\nTokens Parse Fail.'])

        # 獲取：事件資料
        user_id = event.source.user_id
        # 獲取：用戶資料(觸發者)
        profile = linebot_api.get_profile(user_id)
        display_name = profile.display_name # 用戶-名稱

        reply_text = f'{display_name} >>\n' + ' '.join(tokens[1:])
        linebot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

        # todo: Log


    # For: AI
    import json
    #from Meowbot.services.template_chatgpt import Service as ChatGPT
    #from settings import (
    #    CHAT_GPT_KEY,
    #    CHAT_GPT_URL_3,
    #    CHAT_GPT_MODEL_TURBO
    #    #CHAT_GPT_MODEL_DAVINCI_3
    #)
    #ai = ChatGPT(
    #    CHAT_GPT_URL_3,
    #    CHAT_GPT_KEY,
    #    CHAT_GPT_MODEL_TURBO,
    #    #CHAT_GPT_MODEL_DAVINCI_3,
    #    'Test-AI'
    #)
    @command.add(cmds=['#ai'], args={'tokens':None})
    def msg_gpt(linebot_api: LineBotApi, event, args: dict[str,any]):

        tokens = args.get('tokens', ['#fail','[Warnning]\nTokens Parse Fail.'])

        # 獲取：事件資料
        user_id = event.source.user_id
        # 獲取：用戶資料(觸發者)
        profile = linebot_api.get_profile(user_id)
        display_name = profile.display_name # 用戶-名稱

        # 權限檢查
        # todo: 過濾無權限使用持 API 的用戶

        # 呼叫 AI
        response = ai.handle(' '.join(tokens[1:]))
        response_data = response.json()
        print(f'{json.dumps(response_data, indent=4)}')

        # 解析内容
        res_total_tokens = response_data['usage']['total_tokens']
        res_content = response_data['choices'][0]['message']['content']
        res_finish_reason = response_data['choices'][0]['finish_reason']

        # 回應完成原因
        reply_text = f'(Total Tokens: {str(res_total_tokens)})\n{res_content}'
        if res_finish_reason != 'stop':
            reply_text = f'{reply_text}...\n(Reason: {res_finish_reason})'

        # 回復用戶
        linebot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'{display_name} >>\n{reply_text}')
        )

        # todo: Log


