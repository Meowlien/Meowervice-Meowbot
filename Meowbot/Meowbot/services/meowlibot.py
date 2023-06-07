'''
Meowlibot (阿里機器人)：
事件執行處理器 >> [阿里機器人] 對於 Line 事件觸發後的響應行爲
'''

from Meowbot.services.bot import *

class MessageEventHandler(MessageEventHandlerTemplate):
    pass

class FollowEventHandler(FollowEventHandlerTemplate):
    pass

class UnfollowEventHandler(UnfollowEventHandlerTemplate):
    pass

class JoinEventHandler(JoinEventHandlerTemplate):
    pass

class LeaveEventHandler(LeaveEventHandlerTemplate):
    pass

class MemberJoinedEventHandler(MemberJoinedEventHandlerTemplate):
    pass

class MemberLeftEventHandler(MemberLeftEventHandlerTemplate):
    pass

class PostbackEventHandler(PostbackEventHandlerTemplate):
    pass

class BeaconEventHandler(BeaconEventHandlerTemplate):
    pass

class AccountLinkEventHandler(AccountLinkEventHandlerTemplate):
    pass

class ThingsEventHandler(ThingsEventHandlerTemplate):
    pass
