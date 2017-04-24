def start(bot, update):
    # Home message
    msg = "Hello {user_name}! I'm {bot_name}. \n"
    msg += "What would you like to do? \n"
    msg += "Pictograms: \n"
    msg += "========================================\n"
    msg += "/getPicsColor text1,text2,... - List color pictograms that contains textn words \n"
    msg += "/getPicsBW text1,text2,... - List BN pictograms that contains textn words \n"
    msg += "/getPictos - Init wizard to contruct a query for searching pictograms \n"
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
