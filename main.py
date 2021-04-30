from src import market, helper
from conf import config, itemnames
import time
import asyncio
import discord
import http.client
import locale
locale.setlocale(locale.LC_ALL, 'de_DE')

client = discord.Client()
market_ore_time = 0
market_mineral_time = 0
cached_market_ore = ""
cached_market_mineral = ""
market.set_conf(config.market)


async def pricelist(message, types='', region=''):
    if types == '':
        await message.edit(content='Keine Kategorie angegeben. (!markt erze [The Forge])')
        return ''
    types_switch = {
        'erz'       : { 'i': itemnames.ores, 'name': 'ore' },
        'erze'      : { 'i': itemnames.ores, 'name': 'ore' },
        'e'         : { 'i': itemnames.ores, 'name': 'ore' },
        'minerals'  : { 'i': itemnames.minerals, 'name': 'mineral' },
        'mineral'   : { 'i': itemnames.minerals, 'name': 'mineral' },
        'm'         : { 'i': itemnames.minerals, 'name': 'mineral' },
        'moon'      : { 'i': itemnames.moon, 'name': 'moon' },
        'gas'       : { 'i': itemnames.gas, 'name': 'gas' },
        'fullerite' : { 'i': itemnames.fullerite, 'name': 'fullerite' },
    }
    if types not in types_switch:
        await message.edit(content='Unbekannte Kategorie angegeben. (!markt erze [The Forge])')
        return ''
    if region == '':
        region = 'The Forge'
    items = helper.itemlist(types_switch[types]['i'])
    cache_name = types_switch[types]['name']
    cache_store = helper.cache.get(cache_name, region)
    if cache_store is None:
        await message.edit(content="Hole frische Daten")
        cache_store = helper.cache.set(cache_name, region, market.scan(items, region))
    else:
        age = str(int((time.time() - cache_store['ts'])/60))
        await message.edit(content="Hole Daten aus Cache ("+ age +" Minuten alt)")
    return cache_store['data']

@client.event
async def on_ready():
    print('---')


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await message.channel.send('Calculating messages...')
        async for msg in message.channel.history(limit=100):
            if msg.author == message.author:
                counter += 1
        await tmp.edit(content='You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        with message.channel.typing():
            await asyncio.sleep(5)
            await message.channel.send('Done sleeping')
    elif message.content.startswith('!erze') or message.content.startswith('!mineral'):
        await message.channel.send('Bitte nutze !markt <Kategorie> [region]')
    elif message.content.startswith('!id'):
        arg = message.content.split(' ')[1]
        await message.channel.send('Suche ID zu %s' % (arg))
        type_id = market.get_id_esi(arg)
        if type_id == 0:
            await message.channel.send('ID nicht gefunden')
        else:
            await message.channel.send(type_id)
    elif message.content.startswith('!die'):
        if message.author.id == market.conf.owner:
            await message.channel.send('Bye')
            await client.logout()
            await client.close()
    elif message.content.startswith('!deal'):
        order_type = message.content.split(' ')[1]
        type_name = ' '.join(message.content.split(' ')[2:])
        await message.channel.send('Suche Preis zu %s' % (type_name))
        type_id = market.find_deal(order_type,type_name)
        if type_id == -2:
            await message.channel.send('Artikel nicht gefunden')
        elif type_id == 0:
            await message.channel.send('Kein Preis verfügbar')
        else:
            await message.channel.send('{0:,} ISK'.format(type_id))
            await message.channel.send(market.get_order_detail())
    elif message.content.startswith('!market') or message.content.startswith('!markt'):
        tmp = await message.channel.send('Hole Daten. Das wird ein paar Sekunden dauern.')
        if len(message.content.split(' ')) < 2:
            types = ''
        else: 
            types = message.content.split(' ')[1]
        region = ' '.join(message.content.split(' ')[2:])
        data = await pricelist(tmp, types, region)
        await message.channel.send(data)

client.run(config.bot.token)
