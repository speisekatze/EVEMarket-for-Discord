from . import market, helper, tradehubs
from discord.ext import commands
import time
import asyncio
import locale

locale.setlocale(locale.LC_ALL, "de_DE")
bot = commands.Bot(command_prefix='!')
cache_info="Ergebnisse werden für 1 Stunde zwischengespeichert.\nErst nach ablauf der Stunde werden neue Informationen vom Eve-Online Server geholt.\nDas Alter der angezeigten Daten wird angegeben."
region_info="\nStandardregion für den Befehl ist: " + helper.regions.get_by('id', market.marketconfig.region)['name']

def user_is_owner(ctx):
    return ctx.message.author.id == market.marketconfig.owner 

@bot.command(description=cache_info+region_info)
async def erze(ctx):
    """ Kurzform für !markt erze """
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, 'erze')
    await ctx.send(data)

@bot.command(description=cache_info+region_info)
async def mineral(ctx):
    """ Kurzform für !markt mineral """
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, 'mineral')
    await ctx.send(data)

@bot.command(description=cache_info+region_info)
async def mond(ctx):
    """ Kurzform für !markt mond """
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, 'mond')
    await ctx.send(data)

@bot.command(description="Für eine Liste bekannter Kategorien: !typen \n\n" + cache_info + region_info)
async def markt(ctx, kategorien, *region):
    """ Liefert eine Liste aktueller Ver/Einkaufspreise aus der Region """
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    _region = " ".join(region)
    data = await market.pricelist(tmp, kategorien, _region)
    await ctx.send(data)

@bot.command(description="Für eine Liste bekannter Hubs: !tradehubs \n\n" + cache_info)
async def hub(ctx, hub, kategorien):
    """ Liefert eine Liste aktueller Ver/Einkaufspreise von einem Tradehub """
    tmp = await ctx.send(
        "Hole Daten. Das wird ein paar Sekunden dauern."
    )
    data = await market.pricelist(tmp, kategorien, "", hub)
    await ctx.send(data)

@bot.command()
async def typen(ctx):
    """ Liefert eine Liste verfügbarer Kategorien für !markt """
    text = "Verfügbare Kategorien \n"
    text += "```\n"
    text += " * erz, erze, ore, ores - Normale Erze von Asteroiden (Veldspar, Scordite, ..)\n"
    text += " * mineral, minerals - Mineralien (Tritanium, Mexallon, ..)\n"
    text += " * mond, moon - Mond-Mineralien (Cadmium, Cobalt, ..)\n"
    text += " * gas - Gase (Cytoserocin, ..)\n"
    text += "```\n"
    await ctx.send(text)

@bot.command(description="Enthält die Ware Leerzeichen, den Namen in \" schreiben.\n!deal buy \"Compressed Veldspar\" Sinq Laison" + region_info)
async def deal(ctx, art, ware, *region):
    """ Sucht das beste Ver/Ankaufs-Angebot in der Region """
    """ Enthält die Ware Leerzeichen, den Namen in \" schreiben.
        !deal buy \"Compressed Veldspar\" Sinq Laison """
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


@bot.group(name="tradehubs")
async def tr(ctx: commands.Context):
    """ Liefert eine Liste bekannter Tradehubs oder zeigt Informationen zu einem Hub an. """
    if ctx.invoked_subcommand is None:
        list_hubs(ctx)

@tr.command(name="list")
async def list_hubs(ctx):
    """ Liste der bekannten Hubs """
    await ctx.send(tradehubs.list_command())

@tr.command(name="info")
async def info_hubs(ctx, hub):
    """ Informationen zum Hub """
    await ctx.send(tradehubs.info_command(hub))

@bot.command()
@commands.check(user_is_owner)
async def shutdown(ctx):
    await ctx.send("Bye")
    await bot.close()


@bot.command(name='regionen', description="Regionsklassen sind: empire, outlaw, wh, unknown\nWird keine Klasse angegeben, werden die Empire-Regionen angezeigt")
async def region_command(ctx, Klasse='empire'):
    """ Eine Liste bekannter Regionen """
    out_string = "```\n"
    for region in helper.regions.get_by_full('class', Klasse):
        out_string += region["name"] + "\n"
    out_string += "```\n"
    await ctx.send(out_string)
