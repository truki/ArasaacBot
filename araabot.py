'''
Bot that interact with Araasac API to retrieve resources
Developer: @trukise
Email: trukise@gmail.com
'''

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from commands.about import about
from commands.start import start
from commands.pictos import getPictosBN, getPictosColor
import config

import telegram
import urllib3

def echo(bot, update):
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


def main():
    #Configure logging module
    config.logConfig()

    #Configure urllib3 pool depending if we have a proxy web or not
    (proxyEnable, proxyConfiguration) = config.proxySettings()
    if proxyEnable:
        requestPool = urllib3.ProxyManager('http://10.205.96.59:3128/')
    else:
        #requestPool = urllib3.PoolManager()
        requestPool = urllib3.ProxyManager('http://10.205.96.59:3128/')

    # Get ARASAAC API KEY and TELEGRAM_API_KEY
    ARAASAC_API_KEY = config.loadAraasacApiKey(".araasacApiKey")
    TELEGRAM_API_KEY = config.loadTelegramApiKey(".telegramApiKey")

    # Creating an updater object of the Bot
    updater = Updater(TELEGRAM_API_KEY)

    # Declaring handlers and added to dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('getPicsColor', getPictosColor))
    updater.dispatcher.add_handler(CommandHandler('getPicsBN', getPictosBN))

    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
