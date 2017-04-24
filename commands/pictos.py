import json
import urllib3
import config

def getPictosColor(bot, update, args):
    '''
    Functions launched when /getPicsColor command is executed.
    Returns json python dictionary with all color pictograms that contains
    some on the words included in user_data
    '''
    #Configure urllib3 pool depending if we have a proxy web or not
    (proxyEnable, proxyConfiguration) = config.proxySettings()
    if proxyEnable:
        requestPool = urllib3.ProxyManager('http://10.205.96.59:3128/')
    else:
        requestPool = urllib3.PoolManager()
        #global requestPool = urllib3.ProxyManager('http://10.205.96.59:3128/')
    http = requestPool
    req = http.request('GET', 'http://arasaac.org/api/index.php?callback=json&language=ES&word=perro&catalog=colorpictos&nresults=2&thumbnailsize=150&TXTlocate=1&KEY=Xmw49mDsuGduf1qdD8fQ')
    print(req.status)
    print(json.loads(req.data.decode('utf-8')))
    bot.send_message(chat_id=update.message.chat_id,
                     text=json.loads(req.data.decode('utf-8')))

def getPictosBW(bot, update, args):
    '''
    Functions launched when /getPicsBN command is executed.
    Returns a json python dictionary with all BN pictograms that contains
    some on the words included in user_data
    '''
    pass

def getPictos(bot, update):
    '''
    Functions launched when /getPictos command is executed.
    Init a wizard to specified the search of pictograms.
    '''
    pass
