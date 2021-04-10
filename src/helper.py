class items:
    items = None
    ids = None
    names = None
    
    def __init__(self, itemdict):
        self.items = itemdict
        x = dict()
        for a in itemdict:
            x[a['id']] = a['name']
        self.ids = x.copy()
        x = dict()
        for a in itemdict:
            x[a['name']] = a['id']
        self.names = x.copy()
        
    def getById(self, id):
        return self.ids[id]

    def getByName(self, name):
        return self.names[name]

    def getIds(self):
        return self.ids.keys()
    
    def getNames(self):
        return self.ids.values()

def find_max(market):
    global order
    max_price = 0
    for m in market:
        if max_price == 0:
            max_price = float(m['price'])
            order = m
            continue
        if float(m['price']) > max_price:
            max_price = float(m['price'])
            order = m
    return max_price

def find_min(market):
    global order
    min_price = 0
    for m in market:
        if min_price == 0:
            min_price = float(m['price'])
            order = m
            continue
        if float(m['price']) < min_price:
            min_price = float(m['price'])
            order = m
    return min_price