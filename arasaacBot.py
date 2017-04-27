'''
Bot that interact with Araasac API to retrieve resources
Developer: @trukise
Email: trukise@gmail.com
'''
import config
import logging
import urllib3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
import telegram

from commands.about import about
from commands.start import start
import commands.pictos

import inline.pictoInline


ARASAAC_API_KEY = ""
TELEGRAM_API_KEY = ""

global http


def echo(bot, update):
    '''
    more_keyboard = telegram.InlineKeyboardButton("More...", callback_data='1')
    custom_keyboard = [[more_keyboard]]
    reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)
    bot.sendPhoto(chat_id=update.message.chat_id,
                  photo='http://www.arasaac.org/repositorio/originales/7202.png',
                  caption="Perro")
    bot.sendPhoto(chat_id=update.message.chat_id,
                  photo='http://www.arasaac.org/repositorio/originales/7202.png',
                  caption="Perro",
                  reply_markup=reply_markup)
    '''
    pass

def testInlineKeyboard(bot, update):
    keyboard = [[telegram.InlineKeyboardButton("Option 1", callback_data='xxx'),
                 telegram.InlineKeyboardButton("Option 2", callback_data='yyy')],
                [telegram.InlineKeyboardButton("Option 3", callback_data='zzz', token1='zzz', token2='zzzzzz')]]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button_xxx(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

def button_yyy(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

def button_zzz(bot, update, user_data):
    query = update.callback_query
    bot.editMessageText(text="Selected option: {0}. User data: {1}".format(query.data, user_data),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)




def main():
    #Configure logging module
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Starting logger')

    # Get ARASAAC API KEY and TELEGRAM_API_KEY
    global ARASAAC_API_KEY
    ARASAAC_API_KEY = config.loadArasaacApiKey(".arasaacApiKey")

    global TELEGRAM_API_KEY
    TELEGRAM_API_KEY = config.loadTelegramApiKey(".telegramApiKey")

    # Global variable to store user operations
    global users
    users = {}

    http = config.httpPool()
    logger.info(type(http))

    # Create database (sqlite3) bot.db
    config.createBotBatabase("bot.sqlite3")

    # Creating an updater object of the Bot
    updater = Updater(TELEGRAM_API_KEY)

    # Declaring handlers and added to dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('picsColor',
                                                  commands.pictos.getPictosColor,
                                                  pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('picsBW', commands.pictos.getPictosBW,
                                                  pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('getPictos', commands.pictos.getPictos))

    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(CommandHandler('test', testInlineKeyboard))


    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.dispatcher.add_handler(InlineQueryHandler(inline.pictoInline.pictoInline))

    updater.dispatcher.add_handler(CallbackQueryHandler(inline.pictoInline.button_prev, pattern="inline.prev"))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline.pictoInline.button_next, pattern="inline.next"))

    updater.dispatcher.add_handler(CallbackQueryHandler(button_yyy, pattern="yyy"))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_zzz, pattern="zzz", pass_user_data=True,))



    # init Bot
    updater.start_polling()
    updater.idle()
    logger.info("Bot started")


if __name__ == "__main__":
    main()
