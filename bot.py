print('loading system files                ',end='\r')
print('Importing discord                   ',end='\r')
import discord
print('Importing discord.ext.commands      ',end='\r')
from discord.ext import commands
print('Importing sys,traceback,time,logging',end='\r')
import sys, traceback, time, logging
print('Finished importing libraries        ')

logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('bot')

time.perf_counter()
tfile = open('token.txt','r')
token = tfile.read()
def get_prefix(bot, message):
    prefixes = ['?']
    print('Time elapsed: {} ms'.format(time.perf_counter()*1000))
    
    # Allow only ? in dm commands
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description='Discord Bot with Cogs')

# List cogs to be run here
cogs = [
    'cogs.flairs',
    'cogs.misc',
    'cogs.devs',
    'cogs.core',
    'cogs.moderation',
    'cogs.fun'
    ]
print('Time elapsed: {} ms'.format(time.perf_counter()*1000))
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
