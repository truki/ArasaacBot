'''
Bot that interact with Araasac API to retrieve resources
Developer: @trukise
Email: trukise@gmail.com
'''
import config
import logging
import urllib3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import telegram

from commands.about import about
from commands.start import start
import commands.pictos

from inline.pictoInline import pictoInline


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

    # Creating an updater object of the Bot
    updater = Updater(TELEGRAM_API_KEY)

    # Declaring handlers and added to dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('getPicsColor',
                                                  commands.pictos.getPictosColor,
                                                  pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('getPicsBW', commands.pictos.getPictosBW,
                                                  pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('getPictos', commands.pictos.getPictos))

    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.dispatcher.add_handler(InlineQueryHandler(pictoInline))

    # init Bot
    updater.start_polling()
    updater.idle()
    logger.info("Bot started")


if __name__ == "__main__":
    main()
