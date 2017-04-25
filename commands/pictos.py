import config
import json
import logging
import urllib3

logger = logging.getLogger(__name__)


def getPictosColor(bot, update, args):
    '''
    Functions launched when /getPicsColor command is executed.
    Returns json python dictionary with all color pictograms that contains
    some on the words included in user_data
    '''
    query = 'http://arasaac.org/api/index.php?callback=json'
    query += '&language=ES'
    query += '&word='+args[0]
    query += '&catalog=colorpictos&nresults=500&thumbnailsize=100&TXTlocate=1'
    query += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")
    logger.info("QUERY: {}".format(query))
    http = config.httpPool()
    logger.info("Type: {}".format(type(http)))
    req = http.request('GET', query)
    bot.send_message(chat_id=update.message.chat_id,
                     text=json.loads(req.data.decode('utf-8')))

def getPictosBW(bot, update, args):
    '''
    Functions launched when /getPicsBN command is executed.
    Returns a json python dictionary with all BN pictograms that contains
    some on the words included in user_data
    '''
    pass


def getPictos(bot, update):
    '''
    Functions launched when /getPictos command is executed.
    Init a wizard to specified the search of pictograms.
    '''
    pass
