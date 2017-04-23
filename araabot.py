#!/home/sergio/anaconda3/bin/python

'''
Bot that interact with Araasac API to retrieve resources
Developer: @trukise
Email: trukise@gmail.com
'''

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

def loadApiKey(apiKeyFile):
    '''
    Load API KEY of Araaac from hidden file
    '''
    try:
        print(apiKeyFile)
        file = open(apiKeyFile, 'r')
        apiKey = file.read().rstrip('\n')
        return apiKey
    except:
        print("Error")


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

updater = Updater('371175982:AAEr49IbinBITl0KKEqrb1K4MB4rK8Pv8vg')

updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('Hello', hello))
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))


if __name__ == "__main__":
    logConfig()
    API_KEY = loadApiKey(".apiKey")
    print(API_KEY)
    updater.start_polling()
    updater.idle()
