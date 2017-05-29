import ast
import config
import json
import logging
import sqlite3
import telegram

from multiprocessing.pool import ThreadPool


logger = logging.getLogger(__name__)


def insertTranslation(text, language=""):
    '''
    Function that insert into translation table the petition
    | id    | text_to_translate     | language  |
    --------|-----------------------|-----------|
    | 1     |['la','pelota','roja'] | 'ES'      |
    '''

    try:
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO translations (texToTranslate, language) VALUES (?, ?)", (text, language))
        id = c.lastrowid
        logger.info("Translation query of {} inserted with id: {} ".format(text, str(id)))
        conn.commit()
        conn.close()
        return id
    except sqlite3.Error as e:
        logger.error("Error inserting a tranlation, error: {}".format(e.args[0]))
        return -1
    finally:
        conn.close()

def getAndInsertWords(id_translation, word):
    try:
        pictos = []
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO translations_details (idtranslation, word, pictos) VALUES (?, ?, ?)", (id_translation, word, str(pictos)))
        logger.info("Inserted word: {} to translate of tranlation id: {} ".format(word, str(id_translation)))
        conn.commit()
    except sqlite3.Error as e:
        logger.error("Error inserting on translations_details: {}".format(e.args[0]))
    finally:
        if conn:
            conn.close()

def insertWordsToTranslationsDetails(text_to_translate, language,
                                     id_translation):

    conn = config.loadDatabaseConfiguration("bot.sqlite3")
    c = conn.cursor()
    c.execute('SELECT * FROM translations_details WHERE idtranslation= ?', (id_translation,))
    translation_result = c.fetchall()
    conn.close()
    if len(translation_result)==0:
        pool = ThreadPool(len(text_to_translate))
        for word in text_to_translate:
            pool.apply_async(getAndInsertWords, args=(id_translation, word))


def translate(bot, update, args):
    '''
    Command used to translate a little text to pictograms
    '''

    #print("Message : {}".format(update.message))
    #print("User: {}".format(str(update.message.from_user.id)))

    id_translation = insertTranslation(str(args))

    # Fist stage the user must to choose the language
    keyboard = [[telegram.InlineKeyboardButton("Español", callback_data='trans.lang.ES.'+str(id_translation)),
                 telegram.InlineKeyboardButton("English", callback_data='trans.lang.EN.'+str(id_translation)),
                 telegram.InlineKeyboardButton("French", callback_data='trans.lang.FR.'+str(id_translation))],
                [telegram.InlineKeyboardButton("Italian", callback_data='trans.lang.IT.'+str(id_translation)),
                 telegram.InlineKeyboardButton("Catalan", callback_data='trans.lang.CA.'+str(id_translation)),
                 telegram.InlineKeyboardButton("German", callback_data='trans.lang.GE.'+str(id_translation))]
                 ]
    print("id_translation: {}".format(str(id_translation)))

    bot.send_message(chat_id=update.message.chat_id,
                 text="wellcome, translate "+str(args)+"?, choose the language:",
                 reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                 parse_mode=telegram.ParseMode.HTML)


def translate_stage1_language_callback(bot, update):
    '''
    Firs stage in translate command, after choose language
    '''

    query = update.callback_query
    translation = []
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # language specified
    language = data[2]
    # id of translation
    id = int(data[3])

    # get the text to translate from database and update with the language to
    # translate
    try:
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()
        c.execute('SELECT * FROM translations WHERE id=?', (id,))
        translation = c.fetchall()
        logger.info("Translation: {}".format(translation))
        if len(translation)>0:
            translation = translation[0][1] # texToTranslate field
            translation = ast.literal_eval(translation)
            logger.info("Retrieving translations from database: OK, exist!!! {}".format(translation))
            try:
                conn_update = config.loadDatabaseConfiguration("bot.sqlite3")
                c = conn_update.cursor()
                c.execute('''UPDATE translations SET language = ? WHERE id = ?''', (language,id))
                conn_update.commit()
                conn_update.close()
            except sqlite3.Error as e:
                logger.error("An error occurr updating an specified translation id: {} with a language: {}".format(str(id), language))
                logger.error("{}".format(e.args[0]))
            finally:
                if conn_update:
                    conn_update.close()
        else:
            logger.info("UPPS: The translation id: {} don't exists!!!".format(str(id)))
    except sqlite3.Error as e:
        logger.error("An error occur while querying for an specified translation id")
    finally:
        conn.close()

    insertWordsToTranslationsDetails(translation, language, id)

    # making the keyboard with all words that has pictograms
    keyboard = []
    keys = []
    for word in translation:
        keys.append(telegram.InlineKeyboardButton(word, callback_data='trans.word.'+word+'.lang.ES.'+str(id)))

    keyboard.append(keys)


    bot.send_message(chat_id=query.message.chat_id,
                 text="Choose the word button to change pictograms",
                 reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                 parse_mode=telegram.ParseMode.HTML)


def translate_stage2_word_callback(bot, update):
    pass
