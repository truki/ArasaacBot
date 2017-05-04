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
    keyboard = [[telegram.InlineKeyboardButton("Color", callback_data='pics.color.color'),
                 telegram.InlineKeyboardButton("BW", callback_data='pics.color.bw'),
                 telegram.InlineKeyboardButton("Both", callback_data='pics.color.both')]]
    bot.send_message(chat_id=update.message.chat_id,
                     text="<b>Choose type of pictogram: </b>",
                     reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                     parse_mode=telegram.ParseMode.HTML)


def pics_color(bot, update):
    '''
    CallbackQueryHandler that handler the choice of the color, First stage of
    /pics command
    '''

    query = update.callback_query
    print(query)
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # Color specified
    color = data[1]
    print("Color: {}".format(color))

    # Second stage after choose Color --> BW or both
    keyboard = [[telegram.InlineKeyboardButton("ESP", callback_data='pics.language.es.'+color),
                 telegram.InlineKeyboardButton("ENG", callback_data='pics.language.en.'+color),
                 telegram.InlineKeyboardButton("FRE", callback_data='pics.language.fr.'+color)],
                [telegram.InlineKeyboardButton("CAT", callback_data='pics.language.ca.'+color),
                 telegram.InlineKeyboardButton("ITA", callback_data='pics.language.it.'+color),
                 telegram.InlineKeyboardButton("GER", callback_data='pics.language.ge.'+color)
                ]]
    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text="<b>Choose language: </b>",
                     reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                     parse_mode=telegram.ParseMode.HTML)


def pics_language(bot, update):
    '''
    CallbackQueryHandler that handler the choice of the labguage, Second stage
    of /pics command
    '''
    query = update.callback_query
    print(query)
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # Color specified
    language = data[2]
    color = data[3]
    print("Color: {}".format(color))
    print("Language: {}".format(language))

    # Third stage after choose language, now choose kind of search
    # (1-Begin in por 2-Contains 3-End on por 4-Exactly)
    keyboard = [[telegram.InlineKeyboardButton("Start with", callback_data='pics.search.1.'+language+'.'+color),
                 telegram.InlineKeyboardButton("Contains", callback_data='pics.search.2.'+language+'.'+color)],
                [telegram.InlineKeyboardButton("End with", callback_data='pics.search.3.'+language+'.'+color),
                 telegram.InlineKeyboardButton("Exactly", callback_data='pics.search.4.'+language+'.'+color)
                ]]
    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text="<b>Choose a search property: </b>",
                     reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                     parse_mode=telegram.ParseMode.HTML)


def pics_search(bot, update):
    '''
    CallbackQueryHandler that handler the choice of the search property, fourth
    stage of /pics command.
    After choice of search property we send API request to Arasaac Web API
    '''
    query = update.callback_query
    print(query)
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # all query parameters
    search = data[2]
    language = data[3]
    color = data[4]

    print("Color: {}".format(color))
    print("Language: {}".format(language))
    if data[2] == '1':
        print("Search: {}".format("Start with"))
    elif data[2] == '2':
        print("Search: {}".format("Contains"))
    elif data[2] == '3':
        print("Search: {}".format("End with"))
    else:
        print("Search: {}".format("Exactly"))
