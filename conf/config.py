
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
    token = 'ODIwNzY1MDI0MzQyNzY5NzE0.YE56_g.fmxHpb-eaGgxKnbvON7Me4MpXUc'
