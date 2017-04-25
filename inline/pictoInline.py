import config
import json
import logging
import telegram
import urllib3

logger = logging.getLogger(__name__)

def getPictos(language, word):
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
    logger.info("/getPicsColor PICTOS: {}".format(pictos))
    texto = ""
    for picto in pictos:
        texto += '<a href="'+picto['imagePNGURL']+'">'+picto['name']+'</a>'+'\n\n'
    logger.info("TEXTO: {}".format(texto))
    return texto
    #for picto in pictos:
    #    bot.send_message(chat_id=update.message.chat_id,
    #                 text='<a href="'+picto['imagePNGURL']+'">'+picto['name']+'</a>',
    #                 parse_mode=telegram.ParseMode.HTML)


def pictoInline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        telegram.InlineQueryResultArticle(
            id='0',
            title='Spanish',
            input_message_content=telegram.InputTextMessageContent(getPictos('ES', query), parse_mode="HTML", disable_web_page_preview=False)
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='1',
            title='English',
            input_message_content=telegram.InputTextMessageContent('EN')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='2',
            title='French',
            input_message_content=telegram.InputTextMessageContent('FR')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='3',
            title='Catalán',
            input_message_content=telegram.InputTextMessageContent('CA')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='4',
            title='Italian',
            input_message_content=telegram.InputTextMessageContent('IT')
        )
    )
    results.append(
        telegram.InlineQueryResultArticle(
            id='5',
            title='German',
            input_message_content=telegram.InputTextMessageContent('GE')
        )
    )
    logger.info(results)
    bot.answerInlineQuery(update.inline_query.id, results)
