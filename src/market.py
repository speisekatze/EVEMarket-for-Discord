import http.client
import json

#erze
erze = [
    "Compressed Veldspar",
    "Compressed Concentrated Veldspar",
    "Compressed Dense Veldspar",

    "Compressed Scordite",
    "Compressed Condensed Scordite",
    "Compressed Massive Scordite",

    "Compressed Pyroxeres",
    "Compressed Solid Pyroxeres",
    "Compressed Viscous Pyroxeres",

    "Compressed Plagioclase",
    "Compressed Azure Plagioclase",
    "Compressed Rich Plagioclase",

    "Compressed Omber",
    "Compressed Silvery Omber",
    "Compressed Golden Omber",

    "Compressed Kernite",
    "Compressed Luminous Kernite",
    "Compressed Fiery Kernite",

    "Compressed Jaspet",
    "Compressed Pristine Jaspet",
    "Compressed Pure Jaspet",

    "Compressed Hemorphite",
    "Compressed Vivid Hemorphite",
    "Compressed Radiant Hemorphite",

    "Compressed Hedbergite",
    "Compressed Glazed Hedbergite",
    "Compressed Vitric Hedbergite"
]

regions = [
  10000001,
  10000002,
  10000003,
  10000004,
  10000005,
  10000006,
  10000007,
  10000008,
  10000009,
  10000010,
  10000011,
  10000012,
  10000013,
  10000014,
  10000015,
  10000016,
  10000017,
  10000018,
  10000019,
  10000020,
  10000021,
  10000022,
  10000023,
  10000025,
  10000027,
  10000028,
  10000029,
  10000030,
  10000031,
  10000032,
  10000033,
  10000034,
  10000035,
  10000036,
  10000037,
  10000038,
  10000039,
  10000040,
  10000041,
  10000042,
  10000043,
  10000044,
  10000045,
  10000046,
  10000047,
  10000048,
  10000049,
  10000050,
  10000051,
  10000052,
  10000053,
  10000054,
  10000055,
  10000056,
  10000057,
  10000058,
  10000059,
  10000060,
  10000061,
  10000062,
  10000063,
  10000064,
  10000065,
  10000066,
  10000067,
  10000068,
  10000069,
  11000001,
  11000002,
  11000003,
  11000004,
  11000005,
  11000006,
  11000007,
  11000008,
  11000009,
  11000010,
  11000011,
  11000012,
  11000013,
  11000014,
  11000015,
  11000016,
  11000017,
  11000018,
  11000019,
  11000020,
  11000021,
  11000022,
  11000023,
  11000024,
  11000025,
  11000026,
  11000027,
  11000028,
  11000029,
  11000030,
  11000031,
  11000032,
  11000033,
  12000001,
  12000002,
  12000003,
  12000004,
  12000005,
  13000001
]

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
    
    while 1==1:
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
    conn.request('GET','/latest/route/%s/%s/?datasource=tranquility&language=de' % (str(conf.unkah),str(target)),'',conf.headers)

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
    
def get_order_detail():
    global order
    print(order)
    system = get_system(order['system_id'])
    con = get_constellation(system['constellation_id'])
    region = get_region(con['region_id'])
    msg = ''
    msg += 'Verfügbare Anzahl: %s\n' % (order['volume_remain'])
    msg += 'Region: %s\n' % (region['name'])
    msg += 'Sternbild: %s\n' % (con['name'])
    msg += 'System: %s\n' % (system['name'])
    msg += 'Standort: %s\n' % (get_location(order['location_id']))
    msg += '%s Sprünge von Unkah\n' % (str(get_distance(order['system_id'])))
    return msg
    

def find_deal(order_type,type_name):
    global conf
    global conn
    conn = http.client.HTTPSConnection(conf.server)

    type_id = get_id_esi(type_name)
    if type_id == 0:
        return -2
    if order_type == 'buy':
        price = find_max(get_pages(conn,conf.region,type_id,order_type))
    else:
        price = find_min(get_pages(conn,conf.region,type_id,order_type))
    

    return price
    

def run():
    global conf
    global conn
    out_string = ''
    data = '[ "'+'", "'.join(erze)+ '" ]'
    conn = http.client.HTTPSConnection(conf.server)
    conn.request('POST',conf.routes['ids']+'/?datasource=tranquility&language=de',data,conf.headers)

    response = conn.getresponse()
    result = response.read().decode()
    types = json.loads(result)
    i = 1
    for erz in erze:
        price = find_max(get_pages(conn,conf.region,get_id(erz,types['inventory_types']),'buy'))
        total = round(price - (price*0.1),0)
        tabs = '\t'
        if len(erz) > 30:
            out_string += '%s: \t %.2f ISK' % (erz,total) + "\n"
        else:
            out_string += '%s: \t\t\t\t%.2f ISK' % (erz,total) + "\n"
        if 0 == (i % 3):
            out_string += "\n"
        i += 1

    return out_string
