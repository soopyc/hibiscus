import logging

import discord
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
    @commands.has_role('Admin')
    @commands.command(name='warning')
    async def warn(self,ctx,*,stuff: str):
        '''Warn a user
        What a rule-breaker, that you have to use this command...
        '''
        await ctx.send(f'The moderation cog is still being worked on. Ping a person with roles higher than you.')
    
    @commands.command(name='warnings',aliases=['checkuser'])
    async def warnings(self,ctx,userid:str):
        '''Check the warnings for a user. 
        '''
        await ctx.send('Please wait, connecting to the database...',delete_after=5)
        # ping = userid
        uid = userid.replace('<','')
        uid = uid.replace('>','')
        uid = uid.replace("@","")
        uid = uid.replace('!','')
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
            embed.add_field(name=f'Offence {i[2]}:',value=f'{temp1}',inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
'''
cur.execute('select * from offences where id="{}"'.format(str(477792814202224641)))
temp = cur.fetchall()
for i in temp:
    temp1 = str(i[1]).replace('b','')
    temp1 = temp1.replace("'",'')
    embed.add_field(name=f'Offence {i[2]}:',value=f'{temp1}',inline=True)
'''