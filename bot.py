print('loading system files                ',end='\r')
print('Importing discord                   ',end='\r')
import discord
print('Importing discord.ext.commands      ',end='\r')
from discord.ext import commands
print('Importing sys,traceback,time,logging, os',end='\r')
import sys, traceback, time, logging, os
from colorhelper import c
print('Finished importing libraries                         ')

logging.basicConfig(level=logging.INFO, format='{}[%(name)s %(levelname)s] %(message)s'.format(c.info))
logger = logging.getLogger('bot')

'''Remember to set the following environment variables while self-hosting
BOT_TOKEN - Your bot's token
BOT_STAGE - The bot's stage (put self-host as default)
BOT_PREFIX - The bot's default prefix
'''

time.perf_counter()
#tfile = open('token.txt','r')
#token = tfile.read()
token = os.environ["BOT_TOKEN"]

def get_prefix(bot, message):
    prefix = os.environ["BOT_PREFIX"]
    prefixes = [prefix]
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description=f'Blossom {os.environ["BOT_STAGE"]}')

# List cogs to be run here
cogs = [
    'cogs.flairs',
    'cogs.misc',
    'cogs.devs',
    'cogs.core',
    'cogs.moderation',
    'cogs.fun'
    ]
# commands.Bot.remove_command('help')
# Disable cogs
# cogs = []
# Loading cogs
if __name__ == '__main__':
    for cog in cogs:
        logger.info('Loading cog {}'.format(cog))
        bot.load_extension(cog)
        logger.info('Done loading cog {}'.format(cog))

logger.info('Time elapsed: {} ms'.format(time.perf_counter()*1000))
logger.info('Loaded stuffs in {} ms'.format(time.perf_counter()*1000))


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}\n\twith id: {bot.user.id}')
    logger.info(f'Successfully logged in as {bot.user.name} and booted.')

bot.run(token, bot=True, reconnect=True)
ehd = logging.getLogger('exithandler')
ehd.info("Alright, finished bot process and elapsed time is {} seconds".format(time.perf_counter()))
exit(0)
