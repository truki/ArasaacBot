import logging
import sqlite3
import urllib3
from configparser import ConfigParser

logger = logging.getLogger(__name__)
parser = ConfigParser()


def loadDatabaseConfiguration(name):
    try:
        conn = sqlite3.connect(name)
        return conn
    except:
        logger.error("Error connecting to database: {}".format(name))
        exit(-1)

def createBotDatabase(name):
    try:
        conn = loadDatabaseConfiguration(name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS cache
                     (word text, language text, pictos text, dateQuery text, PRIMARY KEY (word, language) )''')
        c.execute('''CREATE TABLE IF NOT EXISTS translations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, texToTranslate text, language text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS translations_details
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, idtranslation INTEGER, word text, position INTEGER, pictos text, pictoWord text, listPictosPath text)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error("Error creating tables on database {}".format(e.args[0]))
    finally:
        if conn:
            conn.close()

def loadArasaacApiKey(araasacApiKeyFile):
    '''
    Load API KEY of Araaac from hidden file
    '''
    try:
        file = open(araasacApiKeyFile, 'r')
        araasacApiKey = file.read().rstrip('\n')
        logger.info("Araasac API KEY Read it: OK")
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
        logger.info("Telegram Bot API KEY Read it: OK")
        return telegramApiKey
    except:
        print("Error reading Telegram Bot API Key: FAIL")


def httpPool():
    parser.read('proxy.ini')
    if parser.get('proxy_settings', 'proxy') == 'yes':
        proxy_url = parser.get('proxy_settings', 'url')
        proxy_port = parser.get('proxy_settings', 'port')
        proxyConfiguration = proxy_url+':'+proxy_port+'/'
        logger.info("Proxy configuration: {}".format(proxyConfiguration))
        return urllib3.ProxyManager(proxyConfiguration)
    else:
        proxyConfiguration = ""
        logger.info("Proxy configuration: NO PROXY")
        return urllib3.PoolManager()
