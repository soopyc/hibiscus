import asyncio
import inspect
import logging
import shlex
import subprocess
import sys

import discord
from discord.ext import commands

from colorhelper import c

from .util.categories import category

logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.devs')

'''Dev commands
'''


class Devs(commands.Cog):
    """Dev commands cog"""
    def __init__(self,bot):
        self.bot = bot

    @category('Developers')
    @commands.command(name='shutdown', aliases=['die'])
    async def die(self,ctx):
        '''Kills the bot.
        '''
        logger.info('Running command die')
        await ctx.send('Shutting down...')
        await ctx.bot.logout()

    @category('Developers')
    @commands.command(name='evaluate',aliases=['eval'])
    async def evaluate(self, ctx, *, code:str):
        '''Run some code.
        The environment currently includes:
         `channel`
         `author`
         `bot`
         `message`
         `channel`
         `ctx`
        '''
        logger.info('Running command eval with parameter(s) {}'.format(code))
        embed = None
        async with ctx.channel.typing():
            result = None
            env = {
                'channel': ctx.channel,
                'author': ctx.author,
                'bot': ctx.bot,
                'message': ctx.message,
                'ctx': ctx,
            }
            env.update(globals())
            try:
                result = eval(code, env)
                if inspect.isawaitable(result):
                    result = await result
                logger.info('eval success: {}'.format(result))
                colour = 0x00FF00
            except Exception as e:
                result = type(e).__name__ + ': ' + str(e)
                logger.error('{}eval error: {}'.format(c.warning,result))
                colour = 0xFF0000

        embed = discord.Embed(colour=colour, title=code, description='```py\n{}```'.format(result))
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        try:
            await ctx.channel.send(embed=embed)
        except discord.errors.Forbidden:
            pass
    @commands.command(name='gitpull')
    async def gitpull(self,ctx):
        async with ctx.channel.typing():
            log=subprocess.run('git pull',stdout=subprocess.PIPE)
            out = str(log.stdout)
            await ctx.send("```diff\n{}```".format(out.replace('b','').replace('\\n','\n')).replace('\'',''))
#    @commands.command(name='gitpush')

def setup(bot): 
    bot.add_cog(Devs(bot))
