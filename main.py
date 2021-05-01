from src import market, helper
from conf import config, itemnames
import time
import asyncio
import discord
from discord.ext import commands
import http.client
import locale

locale.setlocale(locale.LC_ALL, "de_DE")

bot = commands.Bot(command_prefix='!')

def user_is_owner(ctx):
    return ctx.message.author.id == market.marketconfig.owner 

@bot.command(description="Kurzform für !markt erze")
async def erze(ctx):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await pricelist(tmp, 'erze')
    await ctx.send(data)

@bot.command(description="Kurzform für !markt mineral")
async def mineral(ctx):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await pricelist(tmp, 'mineral')
    await ctx.send(data)

@bot.command(description="Kurzform für !markt mond")
async def mond(ctx):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await pricelist(tmp, 'mond')
    await ctx.send(data)

@bot.command(description="Liefert eine Liste aktueller Ver/Einkaufspreise aus der Region")
async def markt(ctx, kategorien, *region):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    _region = " ".join(region)
    data = await pricelist(tmp, kategorien, _region)
    await ctx.send(data)

@bot.command(description="Liefert eine Liste verfügbarer Kategorien für !markt")
async def typen(ctx):
    text = "Verfügbare Kategorien \n"
    text += "```\n"
    text += " * erz, erze, ore, ores - Normale Erze von Asteroiden (Veldspar, Scordite, ..)\n"
    text += " * mineral, minerals - Mineralien (Tritanium, Mexallon, ..)\n"
    text += " * mond, moon - Mond-Mineralien (Cadmium, Cobalt, ..)\n"
    text += " * gas - Gase (Cytoserocin, ..)\n"
    text += "```\n"
    await ctx.send(text)

@bot.command(description="Sucht das beste Ver/Ankaufs-Angebot in der Region\nEnthält die Ware Leerzeichen, den Namen in \" schreiben.\n !deal buy \"Compressed Veldspar\" Sinq Laison")
async def deal(ctx, art, ware, *region):    
    if art not in ['buy', 'sell']:
        await ctx.send("!deal <buy|sell> <Ware>")
    _region = " ".join(region)
    await ctx.send("Suche Preis zu %s" % (ware))
    order = market.find_deal(art, ware, _region)
    if order == -2:
        await ctx.send("Artikel nicht gefunden")
    elif order["price"] == 0:
        await ctx.send("Kein Preis verfügbar")
    else:
        price = locale.format_string("%.2f", float(order["price"]), True, True)
        await ctx.send("{0} ISK".format(price))
        await ctx.send(market.get_order_detail(order))

@bot.command()
@commands.check(user_is_owner)
async def shutdown(ctx):
    await ctx.send("Bye")
    await bot.close()

async def pricelist(message, types="", region=""):
    if types == "":
        await message.edit(content="Keine Kategorie angegeben. (!markt erze [The Forge])")
        return ""
    types_switch = {
        "erz": {"i": itemnames.ores, "name": "ore"},
        "erze": {"i": itemnames.ores, "name": "ore"},
        "e": {"i": itemnames.ores, "name": "ore"},
        "ore": {"i": itemnames.ores, "name": "ore"},
        "ores": {"i": itemnames.ores, "name": "ore"},
        "o": {"i": itemnames.ores, "name": "ore"},
        "minerals": {"i": itemnames.minerals, "name": "mineral"},
        "mineral": {"i": itemnames.minerals, "name": "mineral"},
        "m": {"i": itemnames.minerals, "name": "mineral"},
        "moon": {"i": itemnames.moon, "name": "moon"},
        "mond": {"i": itemnames.moon, "name": "moon"},
        "gas": {"i": itemnames.gas, "name": "gas"},
        "fullerite": {"i": itemnames.fullerite, "name": "fullerite"},
    }
    if types not in types_switch:
        await message.edit(content="Unbekannte Kategorie angegeben. (!markt erze [The Forge])")
        return ""
    if region == "":
        region = "The Forge"
    items = helper.itemlist(types_switch[types]["i"])
    cache_name = types_switch[types]["name"]
    cache_store = helper.cache.get(cache_name, region)
    if cache_store is None:
        await message.edit(content="Hole frische Daten")
        cache_store = helper.cache.set(cache_name, region, market.scan(items, region))
    else:
        age = str(int((time.time() - cache_store["ts"]) / 60))
        await message.edit(content="Hole Daten aus Cache (" + age + " Minuten alt)")
    return cache_store["data"]


bot.run(config.bot.token)