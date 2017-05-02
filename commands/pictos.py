import config
import json
import logging
import telegram
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
    logger.info("/getPicsColor QUERY: {}".format(query))
    http = config.httpPool()
    req = http.request('GET', query)
    datos= json.loads(req.data.decode('utf-8'))
    pictos = datos["symbols"]
    logger.info("/getPicsColor PICTOS: {}".format(pictos))
    for picto in pictos:
        bot.send_message(chat_id=update.message.chat_id,
                     text='<a href="'+picto['imagePNGURL']+'">'+picto['name']+'</a>',
                     parse_mode=telegram.ParseMode.HTML)
        bot.send_audio(chat_id=update.message.chat_id,
                       audio=picto['soundMP3URL'])

def getPictosBW(bot, update, args):
    '''
    Functions launched when /getPicsBN command is executed.
    Returns a json python dictionary with all BN pictograms that contains
    some on the words included in user_data
    '''
    query = 'http://arasaac.org/api/index.php?callback=json'
    query += '&language=ES'
    query += '&word='+args[0]
    query += '&catalog=bwpictos&nresults=500&thumbnailsize=100&TXTlocate=1'
    query += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")
    logger.info("/getPicsBW QUERY: {}".format(query))
    http = config.httpPool()
    req = http.request('GET', query)
    datos= json.loads(req.data.decode('utf-8'))
    pictos = datos["symbols"]
    logger.info("/getPicsBW PICTOS: {}".format(pictos))
    for picto in pictos:
        logger.info("/getPicsBW MP3: {}".format(picto['soundMP3URL']))
        html = '<a href="'+picto['imagePNGURL']+'">'+picto['name']+'</a>\n'
        bot.send_message(chat_id=update.message.chat_id,
                     text=html,
                     parse_mode=telegram.ParseMode.HTML)
        bot.send_audio(chat_id=update.message.chat_id,
                       audio=picto['soundMP3URL'])


def getPics(bot, update):
    # Fist stage choose Color, BW or both
    keyboard = [[telegram.InlineKeyboardButton("Color", callback_data='pics.color'),
                 telegram.InlineKeyboardButton("BW", callback_data='pics.bw'),
                 telegram.InlineKeyboardButton("Both", callback_data='pics.both')]]
    bot.send_message(chat_id=update.message.chat_id,
                     text="<b>Choose type of pictogram: </b>",
                     reply_markup = telegram.ReplyKeyboardMarkup(keyboard),
                     parse_mode=telegram.ParseMode.HTML)


def pics_color(bot, update):
    query = update.callback_query
    print(query)
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    color = data[1]
    print("Color: {}".format(color))
