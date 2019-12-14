import requests
import json

def getCatImage():
    rawres = requests.get('https://api.thecatapi.com/v1/images/search')
    parres = json.loads(rawres.text)
    url = parres[0]["url"]
    return url

async def getCatImageDiscord(ctx):
    async with ctx.channel.typing():
        rawres = requests.get('https://api.thecatapi.com/v1/images/search')
        parres = json.loads(rawres.text)
        url = parres[0]["url"]
        embed = discord.Embed(title="Random Cat Image")
        embed.set_image(url=url)
        embed.set_footer(text="Powered by thecatapi.com!")
        await ctx.send(embed=embed)
