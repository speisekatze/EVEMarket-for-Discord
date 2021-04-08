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
