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
        '''Make a pyramid.
        '''
        count = 1
        string = ''
        temp = []
        for i in range(0,height):
            for k in range(0,count):
                string += '*'
            count += 2
            temp.append(string)
            string = ''
        baselen = len([a for a in temp[len(temp)-1]])
        spaces = int(baselen / 2)
        for i in range(0,height):
            temp3 = ''
            for k in range(0,spaces):
                temp3 += ' '
            temp[i] = temp3 + temp[i]
            spaces -= 1
        string = ''
        for i in temp:
            string += i
            string += '\n'
        await ctx.send(embed=discord.Embed(title='Pyramid Size={}'.format(height),description='```{}```'.format(string),colour=0x00FF00))

def setup(bot):
    bot.add_cog(Fun(bot))
