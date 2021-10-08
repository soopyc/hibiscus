import discord
from discord.ext import commands
import re
import requests
import json
import datetime
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='[%(name)s %(levelname)s] %(message)s')
logger = logging.getLogger('cog.misc')
'''Utility commands
'''


class Utils(commands.Cog):
    """Utility Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say', aliases=['speak'])
    @commands.guild_only()
    async def say(self, ctx, *, ipt: str):
        """
        Make the bot say anything
        Make sure you comply with the rules.
        """
        logger.info(f'Running say command with parameter {ipt}')
        await ctx.send(f'{ipt}')

    @commands.command(name='discordstatus', aliases=['status', 'dstatus'])
    async def discordstatus(self, ctx):
        """
        Check Discord Status
        Checks discord's current status by getting data from status.discordapp.com/index.json
        """
        async with ctx.channel.typing():
            await ctx.send('Please wait...', delete_after=5)
            ret = requests.get('https://status.discordapp.com/index.json')
            rec = json.loads(ret.text)
            if rec['status']['description'] == "All Systems Operational":
                color = 0x00D800
            else:
                color = 0xAA00AA
            embed = discord.Embed(title=rec['status']['description'], colour=color,
                                  description='Data grabbed from [Discord\'s status page](https://status.discordapp.com/index.json).')
            # API Status
            if rec["components"][0]["status"] == "operational":
                embed.add_field(name="API", value="Operational", inline=True)
            else:
                embed.add_field(name="API", value='Not Operational', inline=True)

            # Gateway Status
            if rec["components"][1]["status"] == "operational":
                embed.add_field(name="Gateway", value='Operational', inline=True)
            else:
                embed.add_field(name="Gateway", value='Not Operational', inline=True)
            # CloudFlare Status
            if rec["components"][2]["status"] == "operational":
                embed.add_field(name="CloudFlare", value='Operational', inline=True)
            else:
                embed.add_field(name="CloudFlare", value='Not Operational', inline=True)

            # Media Proxy Status
            if rec["components"][3]["status"] == "operational":
                embed.add_field(name="Media Proxy", value='Operati   onal', inline=True)
            else:
                embed.add_field(name="Gateway", value='Not Operational', inline=True)

            # Voice Server Status
            if rec["components"][3]["status"] == "operational":
                embed.add_field(name="Voice Servers", value='Operational', inline=True)
            else:
                embed.add_field(name="Gateway", value='Not Operational', inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='ping', aliases=['awake', 'check', 'pong'])
    async def ping(self, ctx):
        """
        Ping the bot and check the latency
        """
        logger.info(f'Running command ping with latency {self.bot.latency * 1000}ms')
        # p = subprocess.Popen(["ping","192.168.2.138",'-n','1'], stdout = subprocess.PIPE)
        # timestr = re.compile("Average = [0-9]+ms").findall(str(p.communicate()[0]))
        embed = discord.Embed(title='Bot Ping',
                              description=f'Heartbeat Ping: {self.bot.latency * 1000}ms')
        # \nDatabase Ping:{timestr[0].split(" = ")[1]}')
        await ctx.send(embed=embed)

    @commands.command(name='changelog', aliases=['chglog', 'changes'])
    async def changelog(self, ctx, version: str = None):
        """
        See the change log of the bot.
        version is the v*.*.*
        Version marked with [M] are minor updates.
        use `changelog latest` if you want to see the latest update.
        to see the available sections, use `changelog sections`
        tbh you can try other sections, it might still work.
        """
        async with ctx.channel.typing():
            chglogf = open('changelog.diff', 'r')
            chglog = chglogf.read()
            if version is None:
                return await ctx.send(
                    embed=discord.Embed(title='Changelog', description='```diff\n{}```'.format(chglog)))
            elif version == 'sections':
                temp = re.compile(r'v*.*.* \| [0-9]').findall(chglog)
                sections = ''
                for i in temp:
                    sections += i.split('|')[0].replace(' ', '')
                    sections += ', '
                return await ctx.send(
                    embed=discord.Embed(title='Changelog Sections', description='`\n{}``'.format(sections)))
            elif version == 'latest':
                chgarr = chglog.splitlines()
                temp = re.compile(r'v*.*.* \| [0-9]').findall(chglog)
                ltst = temp[2].split('|')[0].replace(' ', '')
                log = ''
                currln = 0
                lns = []
                for i in range(1, len(chgarr) + 1):
                    print(i)
                    if chgarr[i - 1].split('|')[0] == '{} '.format(ltst):
                        count = int(chgarr[i - 1].split('|')[1])
                        print('Count: {}'.format(count))
                        temp = 0
                        while temp <= count:
                            lns.append(currln + temp)
                            temp += 1
                    currln += 1
                for i in lns:
                    log += chgarr[i]
                    log += '\n'
                return await ctx.send(embed=discord.Embed(title='Changelog of version {}'.format(version),
                                                          description='```diff\n{}```'.format(log)))
            else:
                chgarr = chglog.splitlines()
                log = ''
                currln = 0
                lns = []
                for i in range(1, len(chgarr) + 1):
                    print(i)
                    if chgarr[i - 1].split('|')[0] == '{} '.format(version):
                        count = int(chgarr[i - 1].split('|')[1])
                        print('Count: {}'.format(count))
                        temp = 0
                        while temp <= count:
                            lns.append(currln + temp)
                            temp += 1
                    currln += 1
                for i in lns:
                    log += chgarr[i]
                    log += '\n'
                return await ctx.send(embed=discord.Embed(title='Changelog of version {}'.format(version),
                                                          description='```diff\n{}```'.format(log)))


def setup(bot):
    bot.add_cog(Utils(bot))


'''
currln = 0
lns = []
count = 0
for i in range(1,len(chgarr)+1):
    print(i)
    if chgarr[i-1].split('|')[0] == 'v0.2.1 ':
        count = int(chgarr[i-1].split('|')[1])
        print('Count: {}'.format(count))           
        temp = 0
        while temp <= count:
            print(lns)
            lns.append(currln+temp)
            temp += 1
    currln += 1
for i in lns:
    logs += chgarr[i]
    logs += '\n'
'''
