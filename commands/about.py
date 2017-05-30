def about(bot, update):
    '''
    About me method
    '''
    msg = "*ArasaacBot* is a Telegram Bot that make use os Araasac API,\n"
    msg += "to get and use their resources.\n"
    msg += "It will be useful for profesional who need to get the resources \n"
    msg += "in an easy and fast manner,\n"
    msg += "and for people who have communications or languages disorders"
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     parse_mode="Markdown")

    msg2 = "*ArasaacBot* is an idea of [logopedaSUR](http://www.logopedasur.com), "
    msg2 += "and *Sergio Sánchez Trujillo* @trukise, with the colaboration of [Arasaac](http://arasaac.org)\n "
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg2,
                     parse_mode="Markdown")
