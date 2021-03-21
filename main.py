from src import market
from conf import config
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

async def get_ore(tmp):
    now = time.time()
    global market_ore_time
    global cached_market_ore
    if (now - market_ore_time) > 3600:
        await tmp.edit(content="Hole frische Daten")
        cached_market_ore = market.run(market.erze)
        market_ore_time = now
    else:
        await tmp.edit(content="Hole Daten aus Cache")
    return cached_market_ore


async def get_mineral(tmp):
    now = time.time()
    global market_mineral_time
    global cached_market_mineral
    if (now - market_mineral_time) > 3600:
        await tmp.edit(content="Hole frische Daten")
        cached_market_mineral = market.run(market.erze)
        market_mineral_time = now
    else:
        await tmp.edit(content="Hole Daten aus Cache")
    return cached_market_mineral


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
    elif message.content.startswith('!erze'):
        tmp = await message.channel.send('Hole Daten. Das wird ein paar Sekunden dauern.')
        erze = await get_ore(tmp)
        await message.channel.send(erze)
    elif message.content.startswith('!mineral'):
        tmp = await message.channel.send('Hole Daten. Das wird ein paar Sekunden dauern.')
        mineral = await get_mineral(tmp)
        await message.channel.send(mineral)
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

client.run(config.bot.token)
