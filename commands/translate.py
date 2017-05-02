import telegram


def translate(bot, update, args):
    '''
    Command used to translate a little text to pictograms
    '''
    print("Message : {}".format(update.message))
    print("User: {}".format(str(update.message.from_user.id)))

    # Fist stage the user must to choose the language
    keyboard = [[telegram.InlineKeyboardButton("Español", callback_data='translate.language.ES'),
                 telegram.InlineKeyboardButton("English", callback_data='translate.language.EN'),
                 telegram.InlineKeyboardButton("French", callback_data='translate.language.FR')],
                [telegram.InlineKeyboardButton("Italian", callback_data='translate.language.IT'),
                 telegram.InlineKeyboardButton("Catalan", callback_data='translate.language.CA'),
                 telegram.InlineKeyboardButton("German", callback_data='translate.language.GE')]
                 ]
    bot.send_message(chat_id=update.message.chat_id,
                 text="wellcome, translate '"+str(args)+"?', choose the language:",
                 reply_markup = telegram.ReplyKeyboardMarkup(keyboard),
                 parse_mode=telegram.ParseMode.HTML)


def language_callback(bot, update):
    print("He pasado por language_callback")
