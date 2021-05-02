from conf.regions import hubs
from . import helper
from terminaltables import AsciiTable

hublist = helper.list(hubs)

def list_command(nothing):
    m = [ ["Nummer", "Kurzform", "Region", "Name"], ]
    for hub in hublist.get_all('id'):
        m.append([ str(hub["enum"]), hub["short"], hub["region"], hub["name"] ])
    t = AsciiTable(m)
    t.justify_columns[1] = "left"
    t.justify_columns[2] = "left"
    t.inner_heading_row_border = True
    t.inner_row_border = False
    t.title = "Tradehubs"
    out_string = "```\n" + t.table + "```"
    return out_string

def info_command(lookup):
    hub = hublist.get_by_any(lookup)
    out_string = "```\n"
    out_string += "Name: " + hub['name'] + "\n"
    out_string += "Kurzform: " + hub['short']  + "\n"
    out_string += "Nummer: " + str(hub['enum'])  + "\n"
    out_string += "Region: " + hub['region']  + "\n"
    out_string += "```" + "\n"
    return out_string