
class market:
    #the forge
    region = 10000002
    unkah = 30001679
    server = 'esi.evetech.net'
    routes = {
        'ids' : '/latest/universe/ids',
        'names' : '/latest/universe/names',
        'market' : '/latest/markets/#region#/orders'
        }
    headers = { 'Content-Type' : 'application/json', 'Accept': 'application/json',  'Accept-Language': 'de' }
    
class bot:
    token = 'NTQ2MjcxOTAwNTI4MTQ4NTAw.D0lzig.5VbYouGktNNYhcHg-c61BzIt0e8'
