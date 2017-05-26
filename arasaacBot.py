#!/usr/bin/env python3
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
import commands.translate

import inline.pictoInline


ARASAAC_API_KEY = ""
TELEGRAM_API_KEY = ""

global http


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
    config.createBotDatabase("bot.sqlite3")

    # Creating an updater object of the Bot
    updater = Updater(TELEGRAM_API_KEY)

    # Start command
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # picsColor command - Get pictograms in color that contain the word passed
    updater.dispatcher.add_handler(CommandHandler('picsColor',
                                                  commands.pictos.getPictosColor,
                                                  pass_args=True))

    # picsBW command - Get pictograms in BW that contains the word passed
    updater.dispatcher.add_handler(CommandHandler('picsBW', commands.pictos.getPictosBW,
                                                  pass_args=True))

    # picto command - Command that init a wizard to make a search
    updater.dispatcher.add_handler(CommandHandler('pics',
                                   commands.pictos.getPics,
                                   pass_args=True))

    updater.dispatcher.add_handler(CommandHandler('translate',
                                                  commands.translate.translate,
                                                  pass_args=True))

    updater.dispatcher.add_handler(CommandHandler('about', about))

    updater.dispatcher.add_handler(InlineQueryHandler(inline.pictoInline.pictoInline))

    # CallbackQueryHandlers os /pics command 1º Choose color 2º Choose language
    # 3º search property (start with, contains, end with and exactly)
    updater.dispatcher.add_handler(CallbackQueryHandler(commands.pictos.getPics_stage1_color, pattern="pics.color"))
    updater.dispatcher.add_handler(CallbackQueryHandler(commands.pictos.getPics_stage2_language, pattern="pics.language"))
    updater.dispatcher.add_handler(CallbackQueryHandler(commands.pictos.getPics_stage3_search, pattern="pics.search"))



    updater.dispatcher.add_handler(CallbackQueryHandler(commands.translate.translate_stage1_language_callback, pattern="trans.lang"))

    # init Bot
    updater.start_polling()
    updater.idle()
    logger.info("Bot started")


if __name__ == "__main__":
    main()
