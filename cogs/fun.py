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

    @commands.command(name='pyramid')
    async def pyramid(self,ctx,height:int):
        '''Make a pyramid with size.
        '''
        stars= "*"
        for space_count in range(height- 1, -1, -1):
            print(" " * space_count + stars+ " " * space_count)
            stars+= "**"
        await ctx.send(embed=discord.Embed(title='Pyramid Size={}'.format(height),description='```{}```'.format(stars),colour=0x00FF00))

def setup(bot):
    bot.add_cog(Fun(bot))

'''
def rhombus(height:int):
    for space_count in range(int((height-1)/2), -1, -1):
        spaces = ''
        tempspaces = ''
        for a in range(1,int((height-1)/2)+1):
            tempspaces += ' '
        for i in range(1,space_count+1):
            spaces += ' '
        print("{0}*{0}* (space count: {1})".format(spaces,space_count,tempspaces))
    return
'''