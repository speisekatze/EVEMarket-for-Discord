import time
from conf import regions as data

class itemlist:
    items = None
    ids = None
    names = None

    def __init__(self, itemdict):
        self.items = itemdict
        x = dict()
        for a in itemdict:
            x[a["id"]] = a["name"]
        self.ids = x.copy()
        x = dict()
        for a in itemdict:
            x[a["name"]] = a["id"]
        self.names = x.copy()

    def get_by_id(self, id):
        return self.ids[id]

    def get_by_name(self, name):
        return self.names[name]

    def get_ids(self):
        return self.ids.keys()

    def get_names(self):
        return self.ids.values()

class list:
    items = None
    keys = None
    store = None

    def __init__(self, itemdict):
        self.keys = itemdict[0].keys()
        self.store = {}
        for k in self.keys:
            self.store[k] = {}
            for item in itemdict:
                j = str(item[k]).lower()
                if j not in self.store[k.lower()]:
                    self.store[k.lower()][j] = []
                self.store[k.lower()][j].append(item)
                
    def get_by(self, key, value):
        key = key.lower()
        value = value.lower()
        if (key not in [x.lower() for x in self.keys] 
           or value not in [x.lower() for x in self.store[key.lower()]]):
            return None
        return self.store[key][value][0]

    def get_by_full(self, key, value):
        key = key.lower()
        value = value.lower()
        if (key not in [x.lower() for x in self.keys] 
           or value not in [x.lower() for x in self.store[key.lower()]]):
            return None
        return self.store[key][value]

    def get_by_any(self, value):
        it = None
        value = value.lower()
        for key in self.keys:
            if value in [x.lower() for x in self.get_possible_values(key)]:
                it = self.get_by(key, value)
                break
        return it

    def get_all(self, key):
        key = key.lower()
        if key not in [x.lower() for x in self.keys]:
            return None
        return self.store[key].values()

    def get_possible_values(self, key):
        key = key.lower()
        if key not in [x.lower() for x in self.keys]:
            return None
        return self.store[key].keys()

    def get_keys(self):
        return self.keys
    
    def dump(self):
        return self.store

class _cache:
    store = {}

    def set(self, name, region, data):
        now = time.time()
        if name not in self.store:
            self.store[name] = {}
        self.store[name][region] = {"ts": now, "data": data}
        return self.store[name][region]

    def get(self, name, region):
        now = time.time()
        if (
            name in self.store
            and region in self.store[name]
            and (now - self.store[name][region]["ts"]) < 3600
        ):
            return self.store[name][region]
        return None


def find_max(market, station=0):
    order = {"price": 0.00}
    for m in market:
        if (float(m["price"]) > float(order["price"])) and (
            station == 0 or m["location_id"] == station
        ):
            order = m
    return order


def find_min(market, station=0):
    order = {"price": 0.00}
    for m in market:
        if (
            float(order["price"]) == 0.00 or float(m["price"]) < float(order["price"])
        ) and (station == 0 or m["location_id"] == station):
            order = m
    return order


cache = _cache()
regions = list(data.regions)
