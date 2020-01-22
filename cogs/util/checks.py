import discord
from discord.ext import commands

class checks():
    @staticmethod
    def is_dev():
        async def predicate(ctx):
            return ctx.author.id in [397029587965575170,348921660361146380]
        return commands.check(predicate)