import config
import json
import logging
import telegram
import urllib3

logger = logging.getLogger(__name__)


def getListPictos(language, word):
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
    if len(list) > 0:
        text = '<a href="'+list[pos]['imagePNGURL']+'">'+list[pos]['name']+'</a>'+'\n\n'
    else:
        text = 'No hay resultados'

    return text


def pictoInline(bot, update):
    query = update.inline_query.query
    if not query:
        return

    # reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    def check_reply_markup(picto_list):
        print("longitud: ", len(picto_list))
        print(picto_list)

        if len(picto_list) < 2:
            return None
        else:
            keyboard = [[telegram.InlineKeyboardButton(" < Prev", callback_data='prev.0.'+str([{'CreationDate': '2008-01-14 17:18:09'}])),
                         telegram.InlineKeyboardButton("Next >", callback_data='next.0.'+str([{'CreationDate': '2008-01-14 17:18:09'}]))]]
            return telegram.InlineKeyboardMarkup(keyboard)

    results = list()
    results.append(
        telegram.InlineQueryResultArticle(
            id='0',
            title='Spanish',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('ES', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('ES', query))
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='1',
            title='English',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('EN', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('EN', query))
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='2',
            title='French',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('FR', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('FR', query))
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='3',
            title='Catalan',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('CA', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('CA', query))
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='4',
            title='Italian',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('IT', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('IT', query))

        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='5',
            title='German',
            input_message_content=telegram.InputTextMessageContent(getPictoOnList(getListPictos('GE', query), 0), parse_mode="HTML", disable_web_page_preview=False),
            reply_markup=check_reply_markup(getListPictos('GE', query))
        )
    )
    logger.info(results)
    bot.answerInlineQuery(update.inline_query.id, results)
