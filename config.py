import logging


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
        print("Error reading Araasac API Key: FAIL")


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
