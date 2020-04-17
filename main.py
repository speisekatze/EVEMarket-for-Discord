from lib import market
from conf import config
import time
import asyncio
import discord
import http.client

client = discord.Client()
market_time = 0
cached_market = ""
market.set_conf(config.market)

async def get_market(tmp):
    now = time.time()
    global market_time
    global cached_market
    if (now - market_time) > 3600:
        await tmp.edit(content="Hole frische Daten")
        cached_market = market.run()
        market_time = now
    else:
        await tmp.edit(content="Hole Daten aus Cache")
    return cached_market
    


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
        erze = await get_market(tmp)
        await message.channel.send(erze)
    elif message.content.startswith('!id'):
        conn = http.client.HTTPSConnection(config.market.server)
        arg = message.content.split(' ')[1]
        await message.channel.send('Suche ID zu %s' % (arg))
        type_id = market.get_id_esi(conn,arg)
        if type_id == 0:
            await message.channel.send('ID nicht gefunden')
        else:
            await message.channel.send(type_id)
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
