import ast
import config
import json
import logging
import os
import sqlite3
import telegram
import aux.images

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


def getPictosFromArasaacAPI(language, word):
    '''
    Functions that construct a http query for Arasaac API with a word and a
    language.
    TXTLocate=Exactly matching.
    '''
    pictos = []

    query = 'http://arasaac.org/api/index.php?callback=json'
    query += '&language='+language
    query += '&word='+word
    query += '&catalog=colorpictos&nresults=500&thumbnailsize=100&TXTlocate=4'
    query += '&KEY=' + config.loadArasaacApiKey(".arasaacApiKey")
    http = config.httpPool()
    req = http.request('GET', query)
    datos = json.loads(req.data.decode('utf-8'))
    pictos_temp = datos["symbols"]
    pictos = pictos_temp

    return pictos


def getAndInsertWord(id_translation, language, word, position):
    '''
    Functions that insert (YES now insert) a word of a translation into
    translations_details table.
    Call another function (getPictosFromArasaacAPI) to get pictos field
    (a list with all pictograms objects returned by querying Arasaac API
    with a word and a language)
    Also save a Pictogram with the word on:
    ../images/translation/<id_translation>/pictoText_<word>.png
    '''

    try:
        # make the directory for the translation
        path = os.getcwd()+"/images/translations/"+str(id_translation)+"/"
        os.makedirs(path, exist_ok=True)

        try:
            # Get de Pictogram with the word inside (center)
            pictoText = aux.images.makePictoText(word)
            # make the file name (full path name)
            filenamePictoText = path+"pictoText_"+word+".png"
            # saving the image
            pictoText.save(filenamePictoText)
            logger.info("PictoText: {0} has been saved to {1}.".format(word, filenamePictoText))
        except Exception as e:
            logger.error("while saving the pictoText image: {0},{1}".format(e.args[0], e.args[1]))

        # Get pictos from Arasaac
        pictos = getPictosFromArasaacAPI(language, word)
        conn = config.loadDatabaseConfiguration("bot.sqlite3")
        c = conn.cursor()

        # inserts all path for pictos in this word for a id_translation
        # it is not necessary an order in this list
        listPictosPath = []
        for picto in pictos:
            print("He pasado {}".format(picto))
            urlPicto = picto['imagePNGURL']
            filenamePicto = urlPicto.split('/')[-1]
            print("He pasado2 filenamePicto {}".format(filenamePicto))
            aux.images.getAndSavePicFromUrl(urlPicto, path, filenamePicto)
            listPictosPath.append(path+filenamePicto)
            print("He pasado3 listPictosPath {}".format(listPictosPath))


        # append pictoText path to listPictosPath
        listPictosPath.append(filenamePictoText)

        # insert into translations_details
        c.execute("INSERT INTO translations_details (idtranslation, word, position, pictos, listPictosPath) VALUES (?, ?, ?, ?, ?)", (id_translation, word, position, str(pictos), str(listPictosPath)))
        logger.info("Inserted word: {} to translate of tranlation id: {} ".format(word, str(id_translation)))
        conn.commit()

    except sqlite3.Error as e:
        logger.error("Error inserting on translations_details: {}".format(e.args[0]))
    finally:
        if conn:
            conn.close()

def insertWordsToTranslationsDetails(text_to_translate, language,
                                     id_translation):
    '''
    Functions that call another function to insert all words to
    translations_details table. Run a thread per word
    IMPORTANT: the order (because we use threads) that we insert into table
    perhaps is not the same that the words appearing in the phrase
    '''

    conn = config.loadDatabaseConfiguration("bot.sqlite3")
    c = conn.cursor()
    c.execute('SELECT * FROM translations_details WHERE idtranslation= ?', (id_translation,))
    translation_result = c.fetchall()
    conn.close()
    if len(translation_result)==0:      # cheack if exist
        pool = ThreadPool(len(text_to_translate))
        for word in text_to_translate:
            position = text_to_translate.index(word)
            pool.apply_async(getAndInsertWord, args=(id_translation, language, word, position))
            text_to_translate[text_to_translate.index(word)] = ""


def translate(bot, update, args):
    '''
    Command used to translate a little text to pictograms
    Use: /translate <text to translate>
    Output: An image with a translation and buttons to changes pictograms
    if this is possible
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

    # Send message with text to translate and with a keyboard with
    # all languages options
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
                logger.info("Translation updated with language: {}".format(language))
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

    # After update with the language, inserts all the words into
    # translations_details table
    translation_copy = list(translation)
    insertWordsToTranslationsDetails(translation_copy, language, id)

    # making the keyboard with all words that has pictograms
    keyboard = []
    keys = []
    list_pictos={}
    for word in translation:
        position = translation.index(word)
        # preparing the inline keyboard to show for the phrase to translate
        keys.append(telegram.InlineKeyboardButton(word, callback_data='trans.word.'+word+'.position.'+str(position)+'.lang.ES.'+str(id)))
        translation[position]=""

    logger.info("Completed dictionary with words of translations and its pictograms: {}".format(list_pictos))
    keyboard.append(keys)

    # Send message with (image in the future) and with the buttons
    # that could change every words that can be change (have more than one
    # pictograms available)
    bot.send_message(chat_id=query.message.chat_id,
                 text="Choose the word button to change pictograms",
                 reply_markup = telegram.InlineKeyboardMarkup(keyboard),
                 parse_mode=telegram.ParseMode.HTML)


def translate_stage2_word_callback(bot, update):
    query = update.callback_query
    translation = []
    # obtain callback_data that was sended between '.' character delimiter
    data = query.data.split('.')
    # word specified
    word = data[2]
    # position of the word
    position = int(data[4])
    # language
    language = data[6]
    # id of translation
    id_translation = int(data[7])
    logger.info("Wrord pressed: {0} - position: {1} - id_translation: {2}.".format(word, position, id_translation))
