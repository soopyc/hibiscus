import discord
from discord.ext import commands
from categories import category
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
        await ctx.send(f'{ipt}')

    @commands.command(name='ping', aliases=['awake','check', 'pong'])
    async def ping(self,ctx):
        '''Ping the bot and check the latency'''
        await ctx.send(f'Pong, the bot latency is ``{self.bot.latency*1000}ms``')

def setup(bot):
    bot.add_cog(Utils(bot))