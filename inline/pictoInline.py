import ast
import datetime
import config
import json
import logging
import telegram
import unicodedata
import urllib3

from multiprocessing.pool import ThreadPool

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



def getPictos(lang, word, force=False):
    '''
    Function that return a list of pictos in a specific languages
    '''
    word_ascii_utf8 = unicodedata.normalize('NFD', word).encode('ascii', 'ignore').decode('utf-8')
    pictos = []
    if not(force):
        pictos = existsInCacheAndValid(lang, word)

    # if the return from cache is empty or force is true, send the request
    if len(pictos)<1 or force:
        query = 'http://arasaac.org/api/index.php?callback=json'
        query += '&language='+lang
        query += '&word='+word_ascii_utf8
        query += '&catalog=colorpictos&nresults=500&thumbnailsize=100&TXTlocate=4'
        query += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")
        http = config.httpPool()
        req = http.request('GET', query)
        datos = json.loads(req.data.decode('utf-8'))
        pictos_temp = datos["symbols"]
        if len(pictos_temp) > 0:
            insertPictosDatabase(word, lang, pictos_temp)
        pictos = pictos_temp
    return pictos

def getListPictos(languages, word, force=False):
    '''
    Function that return list of JSON objects (pictograms)
    parameters:
        - languages: list of languages.
        - word: word to search
        - force: if true, force to update cache if the entry exist
    Call another function with threads that return another list of pictos
    for a specific language "getPictos"
    '''

    pictos = []
    pictos_temp = []
    pool = ThreadPool(len(languages))

    # if force is not true, lookfor in cache
    for lang in languages:
        pictos_temp.append(pool.apply_async(getPictos, args=(lang, word, force)))
    pool.close()
    pool.join()
    print("Pictos: {}".format(pictos_temp))
    print("GET: {}".format(pictos_temp[0].get()))
    for p in pictos_temp:
        pictos += p.get()
    print("Pictos_after: {}".format(pictos))
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
    picto_list = getListPictos(['ES','EN','FR','IT','DE','CA'], query, force="false")

    if picto_list != []:
        for picto in picto_list:
            results.append(
                telegram.InlineQueryResultPhoto(id=picto_list.index(picto),
                                                  title=picto['name'],
                                                  photo_url=picto['imagePNGURL'],
                                                  thumb_url=picto['thumbnailURL'],
                                                  caption=picto['name'],
                                                  input_message_content=telegram.InputTextMessageContent(picto['imagePNGURL'])
                )
            )
    else:
        results.append(
            telegram.InlineQueryResultPhoto(id=0,
                                              title="UPPSSS",
                                              photo_url="http://www.arasaac.org/repositorio/originales/5526.png",
                                              thumb_url="http://www.arasaac.org/repositorio/originales/5526.png",
                                              caption="No pictogram were found",
                                              input_message_content=telegram.InputTextMessageContent("No pictogram found")))

    bot.answerInlineQuery(update.inline_query.id, results)
