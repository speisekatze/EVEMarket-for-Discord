from src import market, helper, commands
from conf.config import bot as botconfig

@commands.bot.event
async def on_ready():
    print('Logged in as')
    print(commands.bot.user.name)
    print(commands.bot.user.id)
    print('------')

commands.bot.run(botconfig.token)