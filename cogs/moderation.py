import logging
import re
import subprocess
import time
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions

import mysql.connector
from mysql.connector.errors import OperationalError

logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.moderation')
dblog = logging.getLogger('database')
'''
db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
!!!! Warning: No Password Connection, MUST Restrict User.
Manual Setup is required. Therefore, the bot will not be for total publicity.
'''

class Moderation(commands.Cog):
    '''Moderation Cog'''
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='warnings',aliases=['checkuser','warns'])
    async def warnings(self,ctx,userid:discord.User):
        '''Check the warnings for a user. 
        '''
        await ctx.send('Please wait, connecting to the database...',delete_after=5)
        # ping = userid
        async with ctx.channel.typing():
            try:
                db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            cur = db.cursor()
            uid = userid.id
            dblog.info('Recieved database command `{}`'.format('select * from offences where id="{}"'.format(uid)))
            try:
                cur.execute('select * from offences where id="{}"'.format(str(uid)))
                temp = cur.fetchall()
            except OperationalError as error:
                return await ctx.send(embed=discord.Embed(title='OperationalError',description=f'Exception: \n```{error}```\nAttempting to reconnect to the database...',colour=0xFF0000))
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            if len(temp) == 0:
                embed = discord.Embed(title=f'Warnings for user {userid.name}',description=f'There are no warning(s) for the user {userid.name}.')
            else:
                embed = discord.Embed(title=f'Warning(s) for user {userid.name}',description=f'There are {len(temp)} warning(s) for the user {userid.name}.')
            for i in temp:
                temp1 = str(i[1]).replace("'",'')
                temp2 = [c for c in temp1]
                temp1 = ''
                count = 0
                for k in temp2:
                    if count != 0:
                        temp1 += k
                    count += 1
                dtemp = [yeet for yeet in str(i[3]).replace("'",'')]
                dt = ''
                count = 0
                for k in dtemp:
                    if count != 0:
                        dt += k
                    count += 1
                embed.add_field(name=f'Offence {i[2]}:',value=f'**Details**: {temp1}\n**Warned at:**{dt}',inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='warn')
    @commands.has_permissions(manage_roles=True, manage_messages=True)
    async def warn(self,ctx,user:discord.User,brief:str = 'No brief given.',details:str = 'No details given.', times:int = 1):
        '''Warn a user
        What a massive rulebreaker you have to warn, eh?
        If you want to put a space in the description, make sure to wrap them in quotation marks.
        Times = How many times to warn the user
        If you don't see any messages, check your input or ask @Kenny_#2763
        '''
        await ctx.send('Please wait while the bot retrives data from the database...',delete_after=5)
        async with ctx.channel.typing():
            try:
                db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            cur = db.cursor()
            uid = user.id
            dnt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            logger.info('Warning {}')# for {} time(s)'.format(uid,times))
#            print(f'"{uid}","{details}","{dnt}","{brief}",{int(times)} times')
#            for i in range(0,times):
#            logger.info(f'Warning user {uid} for {i+1} times')
            dblog.info(f'Executing cur.execute(f"select * from offences where id="{uid}")')
            try:
                cur.execute(f'select * from offences where id="{uid}"')
                dblog.info('Executing cur.fetchall')
                result = cur.fetchall()
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            offencecount=len(result)+1
            if brief == " ":
                brief = "No brief given."
            try:
                cur.execute(f'insert into offences (id,details,count,date,brief) values ("{uid}","{details}",{offencecount},"{dnt}","{brief}")')
                db.commit()
                cur.execute(f'select * from offences where id="{uid}"')
                currentoffences = len(cur.fetchall())
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            embed = discord.Embed(title=f'Warned user {user.name}',description=f'User {user.name} warned.',colour=0xFFCC00)
            embed.add_field(name='Reason',value=f'``{details}``')
            embed.add_field(name='Warned by',value=f'{ctx.author.mention}')
            embed.add_field(name='Warned at',value=f'{dnt} UTC+8')
            embed.add_field(name='Current warns',value=currentoffences)
        await ctx.send(embed=embed)

    @warn.error
    async def warnerror(self,error,ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Cannot warn a user',colour=0xFF0000,description='You do not have permission to do so.')
            await ctx.send(embed=embed)
    @commands.command(name="clearwarn",aliases=['clearwarns'])
    @commands.has_permissions(manage_roles=True, manage_messages=True)
    async def clearwarn(self,ctx,user:str):
        '''Removes all warnings from a user
        '''
        try:
            db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
        except Exception as error:
            return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
        cur = db.cursor()
        uid = user.replace('<','').replace('>','').replace("@","").replace('!','')
        command = f"delete from offences where id = '{uid}'"
        try:
            cur.execute(f'select * from offences where id="{uid}"')
            temp = cur.fetchall()
        except Exception as error:
            return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
        warns = len(temp)
        async with ctx.channel.typing():
            cur.execute(command)
            db.commit()
        await ctx.send(embed=discord.Embed(title='Removed warnings.',description=f'Removed {warns} warnings from user {uid}.',colour=0x00FF00))
    
    @clearwarn.error
    async def clearwarnerror(self,error,ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Cannot clear warns',description='You do not have the permission to do so.',colour=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,user:discord.User,reason:str):
        '''Kick a user from the server
        WHO DOES THAT??????
        '''
        async with ctx.channel.typing():
            try:
                db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            cur = db.cursor()
            try:
                await ctx.guild.kick(user=user,reason=reason)
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            embed = discord.Embed(title='User kicked.',description=f'User {user.mention} kicked')
            embed.add_field(name='Reason:',value=reason)
        await ctx.send('_ _',embed=embed)
    @kick.error
    async def kickerror(self,error,ctx):
        embed = discord.Embed(title='Kicking failed',description='Exception:\n```{}```'.format(error),colour=0xFF0000)
        await ctx.send(embed=embed)
    @commands.command(name='ban',aliases=['umbrella','banhammer'])
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx,user:discord.User,reason:str,deletemsg:int=1):
        '''Ban a user
        WHAT THE HECK??!?!?!???!!?! BAD BAN BAN BAN BDNANDABDAJDBudnb
        deletemsg: The number of days worth of messages to delete from the user in the guild. The minimum is 0 and the maximum is 7.
        '''
        async with ctx.channel.typing():
            try:
                db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            cur = db.cursor()
            try:
                await ctx.guild.ban(user,reason=reason)
            except Exception as error:
                return await ctx.send(embed=discord.Embed(title='Command errored.',description=f'Exception: \n```{error}```',colour=0xFF0000))
            embed = discord.Embed(title='User banned.',description=f'User {user.mention} banned.',colour=0xFF0000)
            embed.add_field(name='Reason',value=reason)
        await ctx.send(embed=embed)
    @ban.error
    async def banerror(self,error,ctx):
        embed = discord.Embed(title='Banning failed',description='Exception:\n```{}```'.format(error),colour=0xFF0000)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Moderation(bot))
