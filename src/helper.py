import time


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


def find_max(market):
    order = {"price": 0.00}
    for m in market:
        if float(m["price"]) > float(order["price"]):
            order = m
    return order


def find_min(market):
    order = {"price": 0.00}
    for m in market:
        if float(order["price"]) == 0.00 or float(m["price"]) < float(order["price"]):
            order = m
    return order


cache = _cache()
