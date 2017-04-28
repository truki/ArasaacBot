import ast
import config
import json
import logging
import telegram
import urllib3

logger = logging.getLogger(__name__)


def button_prev(bot, update):
    query = update.callback_query
    print(query)
    # obtain callback_data that was sended between '.' delimiter
    data = query.data.split('.')
    pos = int(data[2])
    print(pos)
    word = data[3]
    print(word)
    language = data[4]
    print(language)

    if pos > 0:

        try:
            conn = config.loadDatabaseConfiguration("bot.sqlite3")
            c = conn.cursor()
            c.execute('SELECT * FROM inlines WHERE word=? AND language=?', (word, language))
            pictos = c.fetchall()[0][2] #list of pictogrmas
            pictos = ast.literal_eval(pictos)
            print(pictos)
        except:
            logger.error("Error en la consulta de la palabra {} en el idioma {}".format(word, language))
        finally:
            conn.close()
        pos = pos - 1
        reply_markup = [[telegram.InlineKeyboardButton(" < Prev", callback_data='inline.prev.'+str(pos)+'.'+word+'.'+language),
                     telegram.InlineKeyboardButton("Next >", callback_data='inline.next.'+str(pos)+'.'+word+'.'+language)]]
        bot.editMessageText(text='<a href="'+pictos[pos]['imagePNGURL']+'">'+pictos[pos]['name']+'</a>'+'\n\n',
                            inline_message_id=query.inline_message_id,
                            parse_mode="HTML",
                            reply_markup = telegram.InlineKeyboardMarkup(reply_markup))

def button_next(bot, update):
    query = update.callback_query
    print(query)
    # obtain callback_data that was sended between '.' delimiter
    data = query.data.split('.')
    pos = int(data[2])
    print(pos)
    word = data[3]
    print(word)
    language = data[4]
    print(language)

    try:
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()
        c.execute('SELECT * FROM inlines WHERE word=? AND language=?', (word, language))
        pictos = c.fetchall()[0][2] #list of pictogrmas
        pictos = ast.literal_eval(pictos)
        print(pictos)
    except:
        logger.error("Error en la consulta de la palabra {} en el idioma {}".format(word, language))
    finally:
        conn.close()
    pos = pos + 1

    reply_markup = [[telegram.InlineKeyboardButton(" < Prev", callback_data='inline.prev.'+str(pos)+'.'+word+'.'+language),
                 telegram.InlineKeyboardButton("Next >", callback_data='inline.next.'+str(pos)+'.'+word+'.'+language)]]

    bot.editMessageText(text='<a href="'+pictos[pos]['imagePNGURL']+'">'+pictos[pos]['name']+'</a>'+'\n\n',
                        inline_message_id=query.inline_message_id,
                        parse_mode="HTML",
                        reply_markup = telegram.InlineKeyboardMarkup(reply_markup))

def insertPictosDatabase(word, language, pictos):
    '''
    Function that insert into inline table pictos of an inline query
    | word  | pictos                |
    --------|-----------------------|
    | ball  |[{picto1},...{picton}] |
    '''

    try:
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO inlines (word, language, pictos) VALUES (?, ?, ?)",(word, language, str(pictos)))
        logger.info("inline query of {} has been inserted".format(word))
        conn.commit()
    except:
        logger.error("Error inserting an inline query")
    finally:
        conn.close()


def getListPictos(language, word):
    '''
    Function that return que API query on a list compound by list of
    JSON objects
    '''

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

    def check_reply_markup(picto_list, language):
        '''
        Function that check if the number of pictos is greater than 1
            yes: create an inline keybord with prev and next buttons
            no: dont create
        in otherwise if the len >= 1 insert de query in inlines tables
        '''
        if len(picto_list) < 2:
            if len(picto_list) > 0:
                insertPictosDatabase(picto_list[0]['name'], language, picto_list)
            return None
        else:
            insertPictosDatabase(picto_list[0]['name'], language, picto_list)
            keyboard = [[telegram.InlineKeyboardButton(" < Prev", callback_data='inline.prev.0.'+picto_list[0]['name']+'.'+language),
                         telegram.InlineKeyboardButton("Next >", callback_data='inline.next.0.'+picto_list[0]['name']+'.'+language)]]
            return telegram.InlineKeyboardMarkup(keyboard)

    results = list()
    results.append(
        telegram.InlineQueryResultArticle(
            id='0',
            title='Spanish',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('ES', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('ES', query), 'ES')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='1',
            title='English',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('EN', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('EN', query), 'EN')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='2',
            title='French',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('FR', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('FR', query), 'FR')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='3',
            title='Catalan',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('CA', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('CA', query), 'CA')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='4',
            title='Italian',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('IT', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('IT', query), 'IT')

        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='5',
            title='German',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('GE', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('GE', query), 'GE')
        )
    )
    logger.info(results)
    bot.answerInlineQuery(update.inline_query.id, results)
