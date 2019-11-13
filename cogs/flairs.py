from discord.ext import commands
import discord
error = ''
try:
    flairs = open('flairs.txt','r')
except FileNotFoundError:
    error = 'notfound'
except:
    error = 'unk'
class Flairs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='f')
    @commands.guild_only()
    async def f(self,ctx, *, ipt: str):
        '''Assign roles to yourself
        ipt = flair name (Check it using ?flairs)
        '''
        await ctx.send('Oops, seems like the Flairs cog is still being worked on! Sorry for the inconvenience, but you have to ask a moderator to give the roles to you.')

    @commands.command(name='flairs')
    @commands.guild_only()
    async def flairs(self,ctx):
        '''Check the available flairs available to add your yourself'''
        await ctx.send('Oops, seems like the Flairs cog is still being worked on! Sorry for the inconvenience, but you have to ask a moderator to tell you the available flairs, which is basically the same as in HTC.')

    @commands.command(name='role',pass_context=True)
    async def role(self, ctx, *, role: discord.Role = None):
        """Give yourself a role, or remove it.
        """
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