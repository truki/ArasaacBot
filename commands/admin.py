#####################################################################
#                                                                   #
# List of commands for bot's adminitration purpose                  #
#                                                                   #
#####################################################################

import os
import sys
import time
import logging

from functools import wraps

logger = logging.getLogger(__name__)

LIST_OF_ADMINS = [45680607, ]

def restricted(func):
    '''
    Decorator define to implement restricted access to some commands
    '''

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = message.from_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

@restricted
def restart(bot, update):
    '''
    Command that restart the bot
    '''

    bot.send_message(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)
