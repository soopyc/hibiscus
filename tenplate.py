import discord
from discord.ext import commands
TOKEN = ''
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(TOKEN)