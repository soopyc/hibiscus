print('loading system files                ',end='\r')
print('Importing discord                   ',end='\r')
import discord
print('Importing discord.ext.commands      ',end='\r')
from discord.ext import commands
print('Importing sys,traceback,time        ',end='\r')
import sys, traceback, time
print('Finished importing datas            ')
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
    'cogs.utils',
    'cogs.devs'
    ]
print('Time elapsed: {} ms'.format(time.perf_counter()*1000))
# Disable cogs
# cogs = []
# Loading cogs
if __name__ == '__main__':
    for cog in cogs:
        print('Loading cog {}'.format(cog),end='\r')
        bot.load_extension(cog)
        print('Done loading cog {}'.format(cog))
        print('Time elapsed: {} ms'.format(time.perf_counter()*1000))
        
print('Time elapsed: {} ms'.format(time.perf_counter()*1000))
print('Loaded stuffs in {} ms'.format(time.perf_counter()*1000))

@bot.event
async def when_mentioned(ctx):
    embed=discord.Embed(title="Hi, I'm Blossom!", description="My default prefix is `?`. Hope this helps!", color=0x176cd5)
    await ctx.send_message(ctx.message.channel, embed=embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}\n\twith id: {bot.user.id}')
    print(f'Successfully logged in as {bot.user.name} and booted.')

bot.run(token, bot=True, reconnect=True)
print("Alright, finished bot process and elapsed time is {} seconds".format(time.perf_counter()))
exit(0)