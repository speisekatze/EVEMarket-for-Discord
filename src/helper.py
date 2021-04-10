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
    order = {'price': 0.00}
    for m in market:
        if float(m['price']) > float(order['price']):
            order = m
    return order

def find_min(market):
    order = {'price': 0.00}
    for m in market:
        if float(order['price']) == 0.00:
            order = m
            continue
        if float(m['price']) < float(order['price']):
            order = m
    return order