import telegram


def translate(bot, update, args):
    '''
    Command used to translate a little text to pictograms
    '''
    print("Message : {}".format(update.message))
    print("User: {}".format(str(update.message.from_user.id)))

    # Fist stage the user must to choose the language
    keyboard = [[telegram.KeyboardButton("Español", callback_data='translate.language.ES'),
                 telegram.KeyboardButton("English", callback_data='translate.language.EN'),
                 telegram.KeyboardButton("French", callback_data='translate.language.FR')],
                [telegram.KeyboardButton("Italian", callback_data='translate.language.IT'),
                 telegram.KeyboardButton("Catalan", callback_data='translate.language.CA'),
                 telegram.KeyboardButton("German", callback_data='translate.language.GE')]
                 ]
    bot.send_message(chat_id=update.message.chat_id,
                 text="wellcome, translate '"+str(args)+"?', choose the language:",
                 reply_markup = telegram.ReplyKeyboardMarkup(keyboard),
                 parse_mode=telegram.ParseMode.HTML)


def language_callback(bot, update):
    print("He pasado por language_callback")
