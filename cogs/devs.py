import asyncio
import inspect
import logging
import shlex
import subprocess
import sys
from datetime import datetime

import discord
import mysql.connector
from discord.ext import commands

from colorhelper import c

logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.devs')

dbhost = "uc13jynhmkss3nve.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
dbuser = "rbo2k37ji007clou"
dbpass = "jffa0eis7dtt4yvm"
dbdb = "pycrhbfzhwacvvo9"
dbport = "3306"
'''Dev commands
'''


class Devs(commands.Cog):
    """Dev commands cog"""
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='shutdown', aliases=['die'])
    async def die(self,ctx):
        '''Kills the bot.
        '''
        logger.info('Running command die')
        await ctx.send('Shutting down...')
        await ctx.bot.logout()

    @commands.is_owner()
    @commands.command(name='herokupush',aliases=['hpush'])
    async def herokupush(self,ctx):
        '''Push the repo to heroku
        Bot Owner Only.
        '''
        herokufile = open('heroku_deploys.log','a+')
        herokufile.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        herokufile.close()
        p = subprocess.Popen('git add .', stdout = subprocess.PIPE)
        p = subprocess.Popen(['git commit','-m','"Update to heroku init from discord."'])
        async with ctx.channel.typing():
            await ctx.send('')
            p = subprocess.Popen(['git push heroku master'], stdout = subprocess.PIPE)
            out = p.stdout.decode()
        await ctx.send(f"```diff\n{out}```")

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
            db = mysql.connector.connect(host=dbhost,user=dbuser,password=dbpass,database=dbdb,port=dbport)
            result = None
            env = {
                'channel': ctx.channel,
                'author': ctx.author,
                'bot': ctx.bot,
                'message': ctx.message,
                'ctx': ctx,
                'db': db,
                'cur': db.cursor() 
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
            out = log.stdout.decode()
            await ctx.send("```diff\n{}```".format(out))
#    @commands.command(name='gitpush')

def setup(bot): 
    bot.add_cog(Devs(bot))
