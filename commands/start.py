def start(bot, update):
    # Home message
    msg = "Hello {user_name}! I'm {bot_name}. \n"
    msg += "What would you like to do? \n"
    msg += "\n"
    msg += "*Get Pictograms??:* \n"
    msg += "==================================\n"
    msg += "/picsColor _<word>_ - List color pictograms that contains the word. \n"
    msg += "/picsBW _<word>_ - List BN pictograms that contains the word. \n"
    msg += "/pics _<word>_ - Wizard to search pictograms. \n"
    msg += "\n"
    msg += "*Translate into pictograms??:* \n"
    msg += "==================================\n"
    msg += "/translate _<words>_ - translate to pictograms the text specified, \n"
    msg += "limit: 8 words \n"
    msg += "The commands transforms the words into pictograms, \n"
    msg += "and show a button per word. These buttons let you \n"
    msg += "to change the pictogram of a specific word, \n"
    msg += "it exits more than one.\n"
    msg += "\n"
    msg += "*Inline mode:* \n"
    msg += "==================================\n"
    msg += "@arasaacbot _<word>_ - After a few seconds you can see a set \n"
    msg += "of thumbnails of pictograms that match the word exactly with \n"
    msg += "the text of them \n"
    msg += "\n"
    msg += "*Other commands:* \n"
    msg += "==================================\n"
    msg += "/about - shows about me information"

    # Send the message
    bot.sendPhoto(chat_id=update.message.chat_id,
                  photo=open('images/ArasaacBot_icon_100x100.png', 'rb'))
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name),
                    parse_mode="Markdown")
