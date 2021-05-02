from . import market, helper, tradehubs
from discord.ext import commands
import time
import asyncio

bot = commands.Bot(command_prefix='!')

def user_is_owner(ctx):
    return ctx.message.author.id == market.marketconfig.owner 

@bot.command(description="Kurzform für !markt erze")
async def erze(ctx):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, 'erze')
    await ctx.send(data)

@bot.command(description="Kurzform für !markt mineral")
async def mineral(ctx):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, 'mineral')
    await ctx.send(data)

@bot.command(description="Kurzform für !markt mond")
async def mond(ctx):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, 'mond')
    await ctx.send(data)

@bot.command(description="Liefert eine Liste aktueller Ver/Einkaufspreise aus der Region")
async def markt(ctx, kategorien, *region):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    _region = " ".join(region)
    data = await market.pricelist(tmp, kategorien, _region)
    await ctx.send(data)

@bot.command(description="Liefert eine Liste aktueller Ver/Einkaufspreise von einem Tradehubs (!tradehubs list)")
async def hub(ctx, hub, kategorien):
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, kategorien, "", hub)
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

@bot.command(name="tradehubs")
async def tradehub(ctx, aktion, hub=""):
    actions = {
        "list": tradehubs.list_command,
        "info": tradehubs.info_command,
    }
    if aktion in actions:
        await ctx.send(actions[aktion](hub))

@bot.command()
@commands.check(user_is_owner)
async def shutdown(ctx):
    await ctx.send("Bye")
    await bot.close()