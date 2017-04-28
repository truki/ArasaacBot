def start(bot, update):
    # Home message
    msg = "Hello {user_name}! I'm {bot_name}. \n"
    msg += "What would you like to do? \n"
    msg += "\n"
    msg += "Get Pictograms??: \n"
    msg += "========================================\n"
    msg += "/picsColor word,... - List color pictograms that contains the words \n"
    msg += "/picsBW word - List BN pictograms that contains the word \n"
    msg += "\n"
    msg += "Translate into pictograms??: \n"
    msg += "========================================\n"
    msg += "/translate - translate to pictograms the text specified, limit: 10 words \n"
    msg += "\n"
    msg += "Inline mode: \n"
    msg += "========================================\n"
    msg += "@arasaacbot <word> - After a time, you must to choose a language, \n"
    msg += "and then you will see a pictogram that contains the word. Then \n"
    msg += "you can navigate with '< prev' and 'next >' buttons if the search \n"
    msg += "has more than one pictogram \n"
    msg += "\n"
    msg += "Other commands: \n"
    msg += "========================================\n"
    msg += "/about - shows about me information"

    # Send the message
    bot.sendPhoto(chat_id=update.message.chat_id,
                  photo=open('images/arasaac_hd_boy_100x100.png', 'rb'))
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))
