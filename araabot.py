'''
Bot that interact with Araasac API to retrieve resources
Developer: @trukise
Email: trukise@gmail.com
'''

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import urllib3

def loadAraasacApiKey(araasacApiKeyFile):
    '''
    Load API KEY of Araaac from hidden file
    '''
    try:
        file = open(araasacApiKeyFile, 'r')
        araasacApiKey = file.read().rstrip('\n')
        print("Araasac API KEY Read it: OK")
        return araasacApiKey
    except:
        print("Error reading Araasac API Key: FAIL" )

def loadTelegramApiKey(telegramApiKeyFile):
    '''
    Load API KEY of Telegram's Bot from hidden file
    '''
    try:
        file = open(telegramApiKeyFile, 'r')
        telegramApiKey = file.read().rstrip('\n')
        print("Telegram Bot API KEY Read it: OK")
        return telegramApiKey
    except:
        print("Error reading Telegram Bot API Key: FAIL")

def proxySettings():
    proxyInput = input("is there a proxy web?[y/n]")
    if proxyInput == 'y':
        proxyConfiguration = input("Introduce proxy settings [(http|https)://<ip>:<port>/] :")
        return (True, proxyConfiguration)
    else:
        proxyConfiguration = ""
        return (False, proxyConfiguration)

def logConfig():
    '''
    Method to configure looging module
    '''
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)

def about(bot, update):
    '''
    About me method
    '''
    update.message.reply_text("Araabot is a bot that make use os Araasac API,to get and use their resources. It will useful for profesional who need to get the resources in an easy and fast manner, and for people who have communications or languages disorders")

def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.username))
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please toalk")
    update.message.reply_text('Hello {}'.format("I'm a bot, please toalk"))

def echo(bot, update):
    update.message.reply_text(update.message.text)


if __name__ == "__main__":
    logConfig()
    (proxyEnable, proxyConfiguration) = proxySettings()
    if proxyEnable:
        requestPool = urllib3.ProxyManager('http://10.205.96.59:3128/')
    else:
        requestPool = urllib3.PoolManager()
        
    ARAASAC_API_KEY = loadAraasacApiKey(".araasacApiKey")
    TELEGRAM_API_KEY = loadTelegramApiKey(".telegramApiKey")

    updater = Updater(TELEGRAM_API_KEY)

    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(CommandHandler('Hello', hello))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()
