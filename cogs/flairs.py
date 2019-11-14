'''
Note from author:
The flair bot would currently not support flair aliases, as it requires me to do a heck ton of stuff, binary searches
and I'm just a busy college student :P
If you can help, feel free to submit a pr.

'''
import json

import discord
from discord.ext import commands

from .util.categories import category

import logging
logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.flairs')
error = ''
flairs = ""
try:
    flairsfile = open('flairs.min.json','r')
    flairs = flairsfile.read()
except FileNotFoundError:
    error = 'notfound'
    logger.critical('Failed to load flair config. If you don\'t want this cog, turn it off in bot.py. Support on turning commands off might be added.')
    raise FileNotFoundError("Flair config not found. Please use the template or the generator.")
except:
    error = 'unk'
##### Flairs Decode #####
'''To See the syntax, visit the readme.md.'''

##### Finish Decode #####
class Flairs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @category('Flairs')
    @commands.command(name='f')
    @commands.guild_only()
    async def f(self,ctx, *, ipt: str):
        '''Assign roles to yourself
        ipt = flair name (Check it using ?flairs)
        '''
        logger.info('Running command f with parameter {}'.format(ipt))
        await ctx.message.delete()
        with open('flairs.json','r') as temp:
            cfg = json.load(temp)
        for i in cfg:
            if i == str(ctx.guild.id):
                for k in cfg[i]:
                    for e in cfg[i][k]:
                        if e != "config":
                            print('Name:{} Value:{}'.format(cfg[i][k][e]["name"],'{}{}'.format(ctx.prefix,e)))
                            if e == ipt:
                                role = discord.utils.get(ctx.guild.roles, id=cfg[i][k][e]["id"])
                                if role not in ctx.message.author.roles:
                                    await ctx.message.author.add_roles(role)
                                    await ctx.send("{} role has been given to {}.".format(role, ctx.message.author.mention),delete_after=5)
                                elif role in ctx.message.author.roles:
                                    await ctx.message.author.remove_roles(role)
                                    await ctx.send("{} role has been removed from {}.".format(role, ctx.message.author.mention),delete_after=5)
        
        # await ctx.send('Oops, seems like the Flairs cog is still being worked on! Sorry for the inconvenience, but you have to ask a moderator to give the roles to you.')

    @category("Flairs")
    @commands.command(name='flairs')
    @commands.guild_only()
    async def flairs(self,ctx):
        '''Check the available flairs available to add your yourself'''
        logger.info('Running command flairs')
        color = 0x00FFF8
        embed = discord.Embed(
            colour=color, 
            title="__**Flairs**__", 
            description='Flairs available to be assigned.'
            )

        with open('flairs.json','r') as temp:
            cfg = json.load(temp)
        for i in cfg:
            if i == str(ctx.guild.id):
                for k in cfg[i]:
                    for e in cfg[i][k]:
                        if e != "config":
                            print('Name:{} Value:{}'.format(cfg[i][k][e]["name"],'{}f {}'.format(ctx.prefix,e)))
                            embed.add_field(name=cfg[i][k][e]["name"], value='{}f {}'.format(ctx.prefix,e),inline=True)
                      
        try:
            await ctx.channel.send(embed=embed)
        except discord.errors.Forbidden:
            pass

    @category('Flairs')
    @commands.command(name='role',pass_context=True)
    @commands.has_role('Admin')
    async def role(self, ctx, *, role: discord.Role = None):
        """Give yourself a role, or remove it.
        """
        logger.info('Running command role with parameter {}'.format(role))
        user = ctx.message.author

        if role is None:
            await ctx.send("You haven't specified a role! ")
        if role not in ctx.message.guild.roles:
            await ctx.send("That role doesn't exist.")
        if role not in ctx.message.author.roles:
            await ctx.send("{} role has been added to {}.".format(role, ctx.message.author.mention))
            await user.add_roles(role)
        elif role in ctx.message.author.roles:
            await user.remove_roles(role)
            await ctx.send("{} role has been removed from {}.".format(role, ctx.message.author.mention))


def setup(bot):
    if error == 'notfound':
        raise FileNotFoundError("Flair config not found. Please use the template or the generator.")
    else:
        bot.add_cog(Flairs(bot))