import logging
import discord
from discord.ext import commands
logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.fun')

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='bran')
    async def bran(self,ctx,user:str,server:str,reason:str = 'The bran hammer'):
        '''Ban A Bad User
        Just jokingly
        '''
        embed = discord.Embed(title='User banned',description=f'User {user} banned from {server} because {reason}',colour=0xFFEE00)
        embed.set_footer(text='WHAT A BAD GUY >:((((((((')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))