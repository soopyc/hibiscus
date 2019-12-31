import discord
from discord.ext import commands
from colorhelper import c

class Administration(commands.Cog):
    '''Administration Cog'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restrictemote",aliases=['resemo'])
    @commands.has_permissions(manage_emojis=True)
    async def restrictemote(ctx,mode,emojis: commands.Greedy[discord.Emoji]):
        '''Restrict Usage of emotes
        Mode
        Docs: https://discordapp.com/developers/docs/resources/emoji#modify-guild-emoji
        '''
        await ctx.send("")
        message = await client.wait_for('message')
    @restrictemote.error
    async def resemoerr(ctx,error):
        await ctx.send(embed=discord.Embed(title="Command Errored.",colour=0x))

def setup(bot):
    bot.add_cog(Administration(bot))
