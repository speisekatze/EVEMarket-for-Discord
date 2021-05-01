import http.client
import json
from src.esi import esi
from src import helper
from conf import regions
from conf.config import market as marketconfig
from terminaltables import AsciiTable
import locale

locale.setlocale(locale.LC_ALL, "de_DE")


def get_order_detail(order):
    eve = esi()
    eve.connect()
    system = query(eve, "system", order["system_id"])
    con = query(eve, "constellation", system["constellation_id"])
    region = query(eve, "region", con["region_id"])
    msg = "```"
    msg += "Verfügbare Anzahl: %s\n" % (order["volume_remain"])
    msg += "Region: %s\n" % (region["name"])
    msg += "Sternbild: %s\n" % (con["name"])
    msg += "System: %s\n" % (system["name"])
    msg += "Standort: %s\n" % (get_location(eve, order["location_id"]))
    msg += "%s Sprünge von %s\n" % (
        str(get_distance(eve, order["system_id"])),
        str(marketconfig.home_name),
    )
    msg += "```"
    return msg


def get_region_id(region):
    regionlist = helper.itemlist(regions.regions)
    if region == "":
        region = "The Forge"
    return regionlist.get_by_name(region)


def find_deal(order_type, type_name, region=""):
    order = None
    eve = esi()
    eve.connect()
    regionid = get_region_id(region)
    type_id = get_esi_id(eve, type_name)
    if type_id == 0:
        return -2
    if order_type == "buy":
        order = helper.find_max(get_orders(eve, regionid, type_id, "buy"))
    else:
        order = helper.find_min(get_orders(eve, regionid, type_id, "sell"))
    return order


def scan(itemlist: helper.itemlist, region=""):
    eve = esi()
    eve.connect()
    regionid = get_region_id(region)
    m = [
        ["Name", "Kauf", "Verkauf"],
    ]
    for item in itemlist.items:
        buy = helper.find_max(get_orders(eve, regionid, item["id"], "buy"))
        total_b = locale.format_string("%.2f", float(buy["price"]), True, True)
        sell = helper.find_min(get_orders(eve, regionid, item["id"], "sell"))
        total_s = locale.format_string("%.2f", float(sell["price"]), True, True)
        m.append([item["name"].replace("Compressed", "comp."), total_b, total_s])
    t = AsciiTable(m)
    t.justify_columns[1] = "right"
    t.justify_columns[2] = "right"
    t.inner_heading_row_border = True
    t.inner_row_border = False
    t.title = region
    out_string = "```" + t.table + "```"
    return out_string


def get_orders(eve, region_id, item_id, order_type):
    page = 1
    json_string = ""
    while True:
        orders = eve.request(
            "market",
            {
                "region": region_id,
                "order_type": order_type,
                "page": page,
                "type_id": item_id,
            },
            "",
        )
        if orders == '{"error":"Requested page does not exist!"}':
            break
        if json_string == "":
            json_string += orders
        else:
            json_string += ", " + orders
        page += 1
    return json.loads("[" + json_string.replace("[", "").replace("]", "") + "]")


def get_esi_id(eve, type_name):
    data = '[ "' + type_name + '" ]'
    result = eve.request("ids", {}, data)
    types = json.loads(result)
    if "inventory_types" in types and len(types["inventory_types"]) > 0:
        return types["inventory_types"][0]["id"]
    elif "station" in types and len(types["station"]) > 0:
        return types["station"]
    else:
        return 0


def get_esi_name(eve, type_id):
    data = "[ " + str(type_id) + " ]"
    result = eve.request("ids", {}, data)
    types = json.loads(result)
    if "name" in types[0]:
        return types[0]["name"]
    else:
        return 0


def get_distance(eve, target):
    result = eve.request("route", {"start": str(marketconfig.home), "end": str(target)})
    systems = json.loads(result)
    return len(systems) - 1


def get_location(eve, location_id):
    if location_id >= 4294967295:
        return "Eine Station eines Spielers"
    else:
        return get_esi_name(eve, location_id)


def get_region(eve, region):
    result = eve.request("region", {"region": region})
    region = json.loads(result)
    return region


def get_constellation(eve, constellation):
    result = eve.request("constellation", {"constellation": constellation})
    constellation = json.loads(result)
    return constellation


def get_system(eve, system):
    result = eve.request("system", {"system": system})
    system = json.loads(result)
    return system


def query(eve, typ, id):
    if typ not in ["system", "region", "constellation"]:
        return None
    result = eve.request(typ, {typ: id})
    return json.loads(result)
