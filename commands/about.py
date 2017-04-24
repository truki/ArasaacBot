def about(bot, update):
    '''
    About me method
    '''
    msg = "Araabot is a bot that make use os Araasac API,\n"
    msg += "to get and use their resources.\n"
    msg += "It will useful for profesional who need to get the resources in an easy and fast manner,\n"
    msg += "and for people who have communications or languages disorders"
    update.message.reply_text(msg)
