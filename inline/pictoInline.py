import ast
import datetime
import config
import json
import logging
import telegram
import urllib3

logger = logging.getLogger(__name__)



def insertPictosDatabase(word, language, pictos):
    '''
    Function that insert into inline table pictos of an inline query
    | word  | pictos                |
    --------|-----------------------|
    | ball  |[{picto1},...{picton}] |
    '''

    date_query = datetime.datetime.now().strftime(format='%D, %H:%M %P')

    try:
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO cache (word, language, pictos, dateQuery) VALUES (?, ?, ?, ?)",(word, language, str(pictos), date_query))
        logger.info("inline query of {} has been inserted".format(word))
        conn.commit()
    except:
        logger.error("Error inserting an inline query")
    finally:
        conn.close()


def existsInCacheAndValid(language, word):
    try:
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()
        c.execute('SELECT * FROM cache WHERE word=? AND language=?', (word, language))
        pictos = c.fetchall()
        print("X_X_X_X_X_X_X_XX_X_X_X_X_ ----->{}".format(pictos))
        if len(pictos)>0:
            logger.info("CACHE: YEAH Caching!!! {}".format(pictos))
            pictos = pictos[0][2] #list of pictogrmas
            logger.info("CACHE: YEAH Caching!!! After Caching 1 {}".format(pictos))
            pictos = ast.literal_eval(pictos)
            logger.info("CACHE: YEAH Caching!!! After Caching 2 {}".format(pictos))
        else:
            logger.info("CACHE: Uppss not cached, new!!!")
    except:
        logger.error("Error searching in cache table database {0} word in {1} language".format(word, language))
    finally:
        conn.close()

    return pictos


def getListPictos(language, word, force=False):
    '''
    Function that return list of JSON objects (pictograms)
    '''

    pictos = []
    print("pictos antes: {}".format(pictos))

    # if force is not true, lookfor in cache
    if not(force):
        pictos = existsInCacheAndValid(language, word)

    print("pictos despues: {}".format(pictos))
    # if the return from cache is empty or force is true, send the request
    if len(pictos)<1 or force:
        query = 'http://arasaac.org/api/index.php?callback=json'
        query += '&language='+language
        query += '&word='+word
        query += '&catalog=colorpictos&nresults=500&thumbnailsize=100&TXTlocate=4'
        query += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")
        logger.info("/getPicsColor QUERY: {}".format(query))
        http = config.httpPool()
        req = http.request('GET', query)
        datos= json.loads(req.data.decode('utf-8'))
        pictos = datos["symbols"]
        if len(pictos) > 0:
            insertPictosDatabase(word, language, pictos)

    return pictos

def getPictoOnList(list, pos):
    '''
    Function that return a text (HTML) with the pictogram on a specified
    position (pos) of a list (list)
    '''

    if len(list) > 0 and pos < len(list):
        text = '<a href="'+list[pos]['imagePNGURL']+'">'+list[pos]['name']+'</a>'+'\n\n'
    else:
        text = 'No hay resultados'

    return text

def pictoInline(bot, update):
    query = update.inline_query.query
    if not query:
        return

    results = list()
    picto_list = getListPictos('ES', query, force="false")

    for picto in picto_list:
        results.append(
            telegram.InlineQueryResultArticle(id=picto_list.index(picto),
                                              title=picto['name'],
                                              input_message_content=telegram.InputTextMessageContent(picto['imagePNGURL'])
            )
        )

    bot.answerInlineQuery(update.inline_query.id, results)

# def pictoInline(bot, update):
#
#     results = list()
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='0',
#             title='Spanish',
#             input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('ES', query), 0), parse_mode="HTML", disable_web_page_preview=False),
#             reply_markup=check_reply_markup(getListPictos('ES', query), 'ES')
#         )
#     )
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='1',
#             title='English',
#             input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('EN', query), 0), parse_mode="HTML", disable_web_page_preview=False),
#             reply_markup=check_reply_markup(getListPictos('EN', query), 'EN')
#         )
#     )
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='2',
#             title='French',
#             input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('FR', query), 0), parse_mode="HTML", disable_web_page_preview=False),
#             reply_markup=check_reply_markup(getListPictos('FR', query), 'FR')
#         )
#     )
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='3',
#             title='Catalan',
#             input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('CA', query), 0), parse_mode="HTML", disable_web_page_preview=False),
#             reply_markup=check_reply_markup(getListPictos('CA', query), 'CA')
#         )
#     )
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='4',
#             title='Italian',
#             input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('IT', query), 0), parse_mode="HTML", disable_web_page_preview=False),
#             reply_markup=check_reply_markup(getListPictos('IT', query), 'IT')
#
#         )
#     )
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='5',
#             title='German',
#             input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('GE', query), 0), parse_mode="HTML", disable_web_page_preview=False),
#             reply_markup=check_reply_markup(getListPictos('GE', query), 'GE')
#         )
#     )
#     logger.info(results)
#     bot.answerInlineQuery(update.inline_query.id, results)
