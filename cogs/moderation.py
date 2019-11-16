import logging
import subprocess
import discord
import re
from datetime import datetime
import mysql.connector
from discord.ext import commands

logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.moderation')
'''
db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
!!!! Warning: No Password Connection, MUST Restrict User.
Manual Setup is required. THerefore, the bot will not be for total publicity.
'''
db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
cur = db.cursor()
class Moderation(commands.Cog):
    '''Moderation Cog'''
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='warnings',aliases=['checkuser'])
    async def warnings(self,ctx,userid:str):
        '''Check the warnings for a user. 
        '''
        await ctx.send('Please wait, connecting to the database...',delete_after=5)
        # ping = userid
        uid = userid.replace('<','').replace('>','').replace("@","").replace('!','')
        logger.info('Recieved database command `{}`'.format('select * from offences where id="{}"'.format(uid)))
        cur.execute('select * from offences where id="{}"'.format(str(uid)))
        temp = cur.fetchall()
        if len(temp) == 0:
            embed = discord.Embed(title=f'Warnings for user {uid}',description=f'There are no warning(s) for the user {uid}.')
        else:
            embed = discord.Embed(title=f'Warning(s) for user {uid}',description=f'There are {len(temp)} warning(s) for the user {uid}.')
        for i in temp:
            temp1 = str(i[1]).replace('b','')
            temp1 = temp1.replace("'",'')
            dt = str(i[4]).replace('b','').replace("'",'')
            embed.add_field(name=f'Offence {i[2]}:',value=f'**Details**: {temp1}\n**Warned at:**{dt}',inline=True)
        await ctx.send(embed=embed)

    @commands.has_role('Admin')
    @commands.command(name='warn')
    async def warn(self,ctx,stuff:str):
        '''Warn a user (see the usage before using.)
        What a massive rulebreaker you have to warn, eh?
        Usage: User Mention/ID|Offence Details|Brief Description
        No spaces between the pipes(|)
        If you want to use the default value, leave a space between the pipes.
        If you don't see any messages, check your input or ask @Kenny_#2763
        '''
        await ctx.send('Please wait while the bot retrives data from the database...',delete_after=5)
        splited = stuff.split('|')
        user = splited[0]
        uid = user.replace('<','').replace('>','').replace("@","").replace('!','')
        details = splited[1]
        brief = splited[2]
        cur.execute(f'select * from offences where id="{uid}"')
        result = cur.fetchall()
        offencecount=len(result)+1
        if brief == " ":
            brief = "No brief given."
        dnt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cur.execute(f'insert into offences (id,details,count,date,brief) values ("{uid}","{details}","{offencecount}","{dnt}",{brief})')
        cur.commit()
        cur.execute(f'select * from offences where id="{uid}"')
        currentoffences = cur.fetchall()
        embed = discord.Embed(title=f'Warned user {user}',description=f'User {user} warned.')
        embed.add_field(name='Reason',value=f'``{details}``')
        embed.add_field(name='Warned by',value=f'{ctx.author}')
        embed.add_field(name='Warned at',value=f'{dnt} UTC+8')
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Moderation(bot))
