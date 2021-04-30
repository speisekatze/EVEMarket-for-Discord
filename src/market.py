import http.client
import json
from src.esi import esi
from src import helper
from conf import regions
from terminaltables import AsciiTable
import locale 
locale.setlocale(locale.LC_ALL, 'de_DE')


conf = { }
conn = object()
order = { }

def set_conf(c):
    global conf
    conf = c

def get_pages(conn,region,type_id,order_type):
    global conf
    json_string = ""
    page = 1
    route = conf.routes['market'].replace('#region#',str(region))
    
    while True:
        conn.request('GET',route+'/?datasource=tranquility&language=de&order_type='+order_type+'&page='+str(page)+'&type_id='+str(type_id),'',conf.headers)

        response = conn.getresponse()
        result = response.read().decode()
        if result == '{"error":"Requested page does not exist!"}':
            break
        if json_string == "":
            json_string += result
        else:
            json_string += ', '+result
        page += 1
    return json.loads('['+json_string.replace('[','').replace(']','')+']')


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

def get_id(type_name,types):
    for i in types:
        if i['name'] == type_name:
            return i['id']

def get_distance(target):
    global conf
    global conn
    conn.request('GET','/latest/route/%s/%s/?datasource=tranquility&language=de' % (str(conf.home),str(target)),'',conf.headers)

    response = conn.getresponse()
    result = response.read().decode()
    systems = json.loads(result)

    return len(systems) - 1

def get_id_esi(type_name):
    global conf
    global conn
    data = '[ "'+type_name+'" ]'
    conn = http.client.HTTPSConnection(conf.server)
    conn.request('POST',conf.routes['ids']+'/?datasource=tranquility&language=de',data,conf.headers)

    response = conn.getresponse()
    result = response.read().decode()
    types = json.loads(result)
    if 'inventory_types' in types and len(types['inventory_types']) > 0:
        return types['inventory_types'][0]['id']
    elif 'station' in types and len(types['station']) > 0:
        return types['station']
    else:
        return 0


def get_name_esi(type_id):
    global conf
    global conn
    data = '[ '+str(type_id)+' ]'
    conn = http.client.HTTPSConnection(conf.server)
    conn.request('POST',conf.routes['names']+'/?datasource=tranquility&language=de',data,conf.headers)

    response = conn.getresponse()
    result = response.read().decode()
    types = json.loads(result)
    
    if 'name' in types[0]:
        return types[0]['name']
    else:
        return 0


def get_location(location_id):
    if location_id >= 4294967295:
        return 'Eine Station eines Spielers'
    else:
        return get_name_esi(location_id)

def get_region(region):
    global conf
    global conn

    conn.request('GET','/latest/universe/regions/'+str(region)+'/?datasource=tranquility&language=de','',conf.headers)
    response = conn.getresponse()
    result = response.read().decode()
    region = json.loads(result)
    
    return region
        
def get_constellation(constellation):
    global conf
    global conn

    conn.request('GET','/latest/universe/constellations/'+str(constellation)+'/?datasource=tranquility&language=de','',conf.headers)
    response = conn.getresponse()
    result = response.read().decode()
    constellation = json.loads(result)
    
    return constellation
    
def get_system(system):
    global conf
    global conn

    conn.request('GET','/latest/universe/systems/'+str(system)+'/?datasource=tranquility&language=de','',conf.headers)
    response = conn.getresponse()
    result = response.read().decode()
    system = json.loads(result)
    
    return system
    
def get_order_detail(order):
    system = get_system(order['system_id'])
    con = get_constellation(system['constellation_id'])
    region = get_region(con['region_id'])
    msg = '```'
    msg += 'Verfügbare Anzahl: %s\n' % (order['volume_remain'])
    msg += 'Region: %s\n' % (region['name'])
    msg += 'Sternbild: %s\n' % (con['name'])
    msg += 'System: %s\n' % (system['name'])
    msg += 'Standort: %s\n' % (get_location(order['location_id']))
    msg += '%s Sprünge von %s\n' % (str(get_distance(order['system_id'])) , str(conf.home_name))
    msg += '```'
    return msg


def get_region_id(region):
    regionlist = helper.itemlist(regions.regions)
    if region == '':
        region = 'The Forge'
    return regionlist.get_by_name(region)

def find_deal(order_type, type_name, region=''):
    order = None
    eve = esi()
    eve.connect()
    regionid = get_region_id(region)
    type_id = get_esi_id(eve, type_name)
    if type_id == 0:
        return -2
    if order_type == 'buy':
        order = helper.find_max(get_orders(eve, regionid, type_id, 'buy'))
    else:
        order = helper.find_min(get_orders(eve, regionid, type_id, 'sell'))
    return order

def scan(itemlist: helper.itemlist, region=''):
    eve = esi()
    eve.connect()
    regionid = get_region_id(region)
    m = [ ['Name', 'Kauf', 'Verkauf'], ]
    for item in itemlist.items:
        buy = helper.find_max(get_orders(eve, regionid, item['id'], 'buy'))
        total_b = locale.format_string('%.2f', float(buy['price']), True, True)
        sell = helper.find_min(get_orders(eve, regionid, item['id'], 'sell'))
        total_s = locale.format_string('%.2f', float(sell['price']), True, True)
        m.append([item['name'].replace('Compressed', 'comp.'), total_b, total_s])
    t = AsciiTable(m)
    t.justify_columns[1] = 'right'
    t.justify_columns[2] = 'right'
    t.inner_heading_row_border = True
    t.inner_row_border = False
    t.title = region
    out_string = '```' + t.table + '```'
    return out_string

def get_orders(eve, region_id, item_id, order_type):
    page = 1
    json_string = ""
    while True:
        orders = eve.request('market', {'region': region_id, 'order_type': order_type, 'page': page, 'type_id': item_id }, '')
        if orders == '{"error":"Requested page does not exist!"}':
            break
        if json_string == "":
            json_string += orders
        else:
            json_string += ', '+orders
        page += 1
    return json.loads('['+json_string.replace('[','').replace(']','')+']')

def get_esi_id(eve, type_name):
    data = '[ "'+type_name+'" ]'
    conn = http.client.HTTPSConnection(conf.server)
    conn.request('POST',conf.routes['ids']+'/?datasource=tranquility&language=de',data,conf.headers)
    eve.request('ids', {}, data)

    response = conn.getresponse()
    result = response.read().decode()
    types = json.loads(result)
    if 'inventory_types' in types and len(types['inventory_types']) > 0:
        return types['inventory_types'][0]['id']
    elif 'station' in types and len(types['station']) > 0:
        return types['station']
    else:
        return 0
