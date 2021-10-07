# from . import channel, gateway, guild, interaction, message, user, bot
from .bot import *
from .gateway import *
from .channel import *
from .message import *
from .guild import *

def set_globals(t, b, l):
    global token
    global user_bot
    global main_loop
    token = t
    user_bot = b
    main_loop = l