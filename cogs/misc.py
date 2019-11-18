import discord
from discord.ext import commands
import re
import subprocess
import logging
logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.misc')
'''Utility commands
'''

class Utils(commands.Cog):
    """Utility Cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say', aliases=['speak'])
    @commands.guild_only()
    async def say(self,ctx, *, ipt: str):
        '''Make the bot say anything
        Make sure you comply with the rules.
        '''
        logger.info(f'Running say command with parameter {ipt}')
        await ctx.send(f'{ipt}')

    @commands.command(name='ping', aliases=['awake','check', 'pong'])
    async def ping(self,ctx):
        '''Ping the bot and check the latency'''
        logger.info(f'Running command ping with latency {self.bot.latency*1000}ms')
        p = subprocess.Popen(["ping.exe","192.168.2.138",'-n','1'], stdout = subprocess.PIPE)
        timestr = re.compile("Average = [0-9]+ms").findall(str(p.communicate()[0]))
        embed = discord.Embed(title='Bot Ping',description=f'Heartbeat Ping: {self.bot.latency*1000}ms \nDatabase Ping:{timestr[0].split(" = ")[1]}')
        await ctx.send(embed=embed)
    
    @commands.command(name='changelog',aliases=['chglog','changes'])
    async def changelog(self,ctx,version:str=None):
        '''See the change log of the bot.
        version is the v*.*.*
        Version marked with [M] are minor updates.
        tbh you can try other sections, it might still work.
        '''
        if version == None:
            chglogf = open('changelog.diff','r')
            chglog = chglogf.read()
            return await ctx.send(embed=discord.Embed(title='Changelog',description='```diff\n{}```'.format(chglog)))
        else:
            return await ctx.send('Work in progress.')
def setup(bot):
    bot.add_cog(Utils(bot))