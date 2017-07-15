import config
import json
import logging
import telegram

logger = logging.getLogger(__name__)


def getPictosFromArasaac(query_url):
    '''
    Function that get an url with the API web request
    and return an array of json objects (answer)
    '''
    print("QUERYURL: {}".format(query_url))
    http = config.httpPool()
    # GET request
    req = http.request('GET', query_url)
    # load the answer in JSON format
    data = json.loads(req.data.decode('utf-8'))
    # only return 'symbols' field (array of JSON objects)
    pictograms = data["symbols"]
    return pictograms


def getPictosFromQuery(word, color, language, search, nresults=500, wordType=2):
    '''
    Functions that return an array of json objects with pictograms
    The API query is made of parameters defined in function declarations:
    word:       word to search
    color:      BW, color, both
    language:   ES, EN, FR, CA, IT, GE
    search:     1-start with, 2-contains, 3-end with, 4-Exactly
    nresults:   num of result that return de query to web API, set to 500 by
                default to get all the posibilities.
    wordType:   1-Nombres propios, 2-Nombres Comunes, 3- Verbos,
                4- Descriptivos, 5- Contenido Social, 6-Miscelánea
    '''
    if color == 'both':
        # contruct api request for pictograms on color catalog
        catalog = 'colorpictos'
        query_color_url = 'http://arasaac.org/api/index.php?callback=json'
        query_color_url += '&language='+language
        query_color_url += '&word='+word
        query_color_url += '&catalog='+catalog+'&nresults='+str(nresults)+'&thumbnailsize=50'
        query_color_url += '&TXTlocate='+search
        query_color_url += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")
        pictograms_color = getPictosFromArasaac(query_color_url)
        # construct api request for pictograms on bw catalog
        catalog = 'bwpictos'
        query_bw_url = 'http://arasaac.org/api/index.php?callback=json'
        query_bw_url += '&language='+language
        query_bw_url += '&word='+word
        query_bw_url += '&catalog='+catalog+'&nresults='+str(nresults)+'&thumbnailsize=50'
        query_bw_url += '&TXTlocate='+search
        query_bw_url += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")
        pictograms_bw = getPictosFromArasaac(query_bw_url)
        # concatenate both array of pictograms
        pictograms = pictograms_color + pictograms_bw
    else:
        if color == 'color':
            catalog = 'colorpictos'
        else:
            catalog == 'bwpictos'

        query_url = 'http://arasaac.org/api/index.php?callback=json'
        query_url += '&language='+language
        query_url += '&word='+word
        query_url += '&catalog='+catalog+'&nresults='+str(nresults)+'&thumbnailsize=50'
        query_url += '&TXTlocate='+search
        query_url += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")

        pictograms = getPictosFromArasaac(query_url)

    return pictograms

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
        if 'soundMP3URL' in picto.keys():
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
    if len(pictos) > 0:
        for picto in pictos:
            html = '<a href="'+picto['imagePNGURL']+'">'+picto['name']+'</a>\n'
            bot.send_message(chat_id=update.message.chat_id,
                         text=html,
                         parse_mode=telegram.ParseMode.HTML)
            if 'soundMP3URL' in picto.keys():
                bot.send_audio(chat_id=update.message.chat_id,
                               audio=picto['soundMP3URL'])
    else:
        bot.sendPhoto(chat_id=update.message.chat_id,
                          photo=open('images/ArasaacBot_icon_100x100.png', 'rb'))
        bot.send_message(chat_id=update.message.chat_id,
                             text="*No pictograms were founded!!* \n launch another query",
                             parse_mode=telegram.ParseMode.MARKDOWN)

def getPics(bot, update, args):
    '''
    Fist stage of /pics wizard choose Color, BW or both
    '''
    if len(args)>0:
        keyboard = [[telegram.InlineKeyboardButton("Color", callback_data='pics.color.color.'+args[0]),
                     telegram.InlineKeyboardButton("BW", callback_data='pics.color.bw.'+args[0]),
                     telegram.InlineKeyboardButton("Both", callback_data='pics.color.both.'+args[0])]]
        bot.send_message(chat_id=update.message.chat_id,
                         text="<b>Choose type of pictogram: </b>",
                         reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                         parse_mode=telegram.ParseMode.HTML)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="<b>Upss you forget the word !! </b>",
                         parse_mode=telegram.ParseMode.HTML)


def getPics_stage1_color(bot, update):
    '''
    CallbackQueryHandler that handler the choice of the color, First stage of
    /pics command
    '''

    query = update.callback_query
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # Color specified
    color = data[2]
    #word specified
    word = data[3]


    # Second stage after choose Color --> BW or both
    keyboard = [[telegram.InlineKeyboardButton("ESP", callback_data='pics.language.ES.'+color+'.'+word),
                 telegram.InlineKeyboardButton("ENG", callback_data='pics.language.EN.'+color+'.'+word),
                 telegram.InlineKeyboardButton("FRE", callback_data='pics.language.FR.'+color+'.'+word)],
                [telegram.InlineKeyboardButton("CAT", callback_data='pics.language.CA.'+color+'.'+word),
                 telegram.InlineKeyboardButton("ITA", callback_data='pics.language.IT.'+color+'.'+word),
                 telegram.InlineKeyboardButton("GER", callback_data='pics.language.GE.'+color+'.'+word)
                ]]
    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text="<b>Choose language: </b>",
                     reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                     parse_mode=telegram.ParseMode.HTML)


def getPics_stage2_language(bot, update):
    '''
    CallbackQueryHandler that handler the choice of the labguage, Second stage
    of /pics command
    '''
    query = update.callback_query
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # Color specified
    language = data[2].upper()
    color = data[3]
    word = data[4]


    # Third stage after choose language, now choose kind of search
    # (1-Begin in por 2-Contains 3-End on por 4-Exactly)
    keyboard = [[telegram.InlineKeyboardButton("Start with", callback_data='pics.search.1.'+language+'.'+color+'.'+word),
                 telegram.InlineKeyboardButton("Contains", callback_data='pics.search.2.'+language+'.'+color+'.'+word)],
                [telegram.InlineKeyboardButton("End with", callback_data='pics.search.3.'+language+'.'+color+'.'+word),
                 telegram.InlineKeyboardButton("Exactly", callback_data='pics.search.4.'+language+'.'+color+'.'+word)
                ]]
    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text="<b>Choose a search property: </b>",
                     reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                     parse_mode=telegram.ParseMode.HTML)


def getPics_stage3_search(bot, update):
    '''
    CallbackQueryHandler that handler the choice of the search property, third
    stage of /pics command.
    After choice of search property we send API request to Arasaac Web API
    '''
    query = update.callback_query
    print(query)
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # all query parameters
    search = data[2]
    language = data[3].upper()
    color = data[4]
    word = data[5]

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

    pictograms = getPictosFromQuery(word, color, language, search)

    if len(pictograms) > 0:
        for picto in pictograms:
            bot.sendPhoto(chat_id=query.message.chat_id,
                          photo=picto['imagePNGURL'],
                          caption=picto['name'])
    else:
        bot.sendPhoto(chat_id=query.message.chat_id,
                      photo=open('images/ArasaacBot_icon_100x100.png', 'rb'))
        bot.send_message(chat_id=query.message.chat_id,
                         text="*No pictograms were founded!!* \n launch another query",
                         parse_mode=telegram.ParseMode.MARKDOWN)
