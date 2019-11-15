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

class Moderation(commands.Cog):
    '''Moderation Cog'''
    def __init__(self,bot):
        self.bot = bot

    db = mysql.connector.connect(host="localhost",user="localuser",database="cogbot_schema",port=7000)
    @commands.has_role('Admin')
    @commands.command(name='warning')
    async def warn(self,ctx,*,stuff: str):
        '''Warn a user
        What a rule-breaker, that you have to use this command...
        '''
        await ctx.send(f'The moderation cog is still being worked on. Ping a person with roles higher than you.')
