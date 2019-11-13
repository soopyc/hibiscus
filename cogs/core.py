import datetime
from discord.ext import commands
import discord
from .util.categories import category
'''Core commands    
'''


class Core(commands.Cog):
    """Core commands cog"""
    def __init__(self,bot):
        self.bot = bot

    @category('info')
    @commands.command()
    async def help(self, ctx, *args):
        '''This help message :D'''
        cmds = {i for i in ctx.bot.all_commands.values()}
        if len(args) == 0:
            d = ''#'**TWOWBot help:**'

            cats = {}
            for cmd in cmds:
                if not hasattr(cmd, 'category'):
                    cmd.category = 'Misc'
                if cmd.category not in cats:
                    cats[cmd.category] = []
                cats[cmd.category].append(cmd)

            d += '\n**Categories:**\n'
            for cat in cats:
                d += '**`{}`**\n'.format(cat)
            d += '\nUse `{}help <category>` to list commands in a category'.format(ctx.prefix)
            d += '\nUse `{}help <command>` to get indepth help for a command\n'.format(ctx.prefix)
        elif len(args) == 1:
            cats = {}
            for cmd in cmds:
                if not hasattr(cmd, 'category'):
                    cmd.category = 'Misc'
                if cmd.category not in cats:
                    cats[cmd.category] = []
                cats[cmd.category].append(cmd)
            if args[0].title() in cats:
                d = 'Commands in caterogy **`{}`**:\n'.format(args[0])
                for cmd in sorted(cats[args[0].title()], key=lambda x:x.name):
                    d += '\n  `{}{}`'.format(ctx.prefix, cmd.name)

                    brief = cmd.brief
                    if brief is None and cmd.help is not None:
                        brief = cmd.help.split('\n')[0]

                    if brief is not None:
                        d += ' - {}'.format(brief)
                d += '\n'
            else:
                if args[0] not in ctx.bot.all_commands:
                    d = 'Command not found.'
                else:
                    cmd = ctx.bot.all_commands[args[0]]
                    d = 'Help for command `{}`:\n'.format(cmd.name)
                    d += '\n**Usage:**\n'

                    if type(cmd) != commands.core.Group:
                        params = list(cmd.clean_params.items())
                        p_str = ''
                        for p in params:
                            if p[1].default == p[1].empty:
                                p_str += ' [{}]'.format(p[0])
                            else:
                                p_str += ' <{}>'.format(p[0])
                        d += '`{}{}{}`\n'.format(ctx.prefix, cmd.name, p_str)
                    else:
                        d += '`{}{} '.format(ctx.prefix, cmd.name)
                        if cmd.invoke_without_command:
                            d += '['
                        else:
                            d += '<'
                        d += '|'.join(cmd.all_commands.keys())
                        if cmd.invoke_without_command:
                            d += ']`\n'
                        else:
                            d += '>`\n'
                    
                    d += '\n**Description:**\n'
                    d += '{}\n'.format('None' if cmd.help is None else cmd.help.strip())

                    if cmd.aliases:
                        d += '\n**Aliases:**'
                        for alias in cmd.aliases:
                            d += '\n`{}{}`'.format(ctx.prefix, alias)

                        d += '\n'
        else:
            d = ''
            cmd = ctx.bot
            cmd_name = ''
            for i in args:
                i = i.replace('@', '@\u200b')
                if hasattr(cmd, 'all_commands') and i in cmd.all_commands:
                    cmd = cmd.all_commands[i]
                    cmd_name += cmd.name + ' '
                else:
                    if cmd == ctx.bot:
                        d += 'Command not found.'
                    else:
                        d += '`{}` has no sub-command `{}`.'.format(cmd.name, i)
                    break
            if cmd != ctx.bot:
                d = 'Help for command `{}`:\n'.format(cmd_name)
                d += '\n**Usage:**\n'

                if type(cmd) != commands.core.Group:
                    params = list(cmd.clean_params.items())
                    p_str = ''
                    for p in params:
                        if p[1].default == p[1].empty:
                            p_str += ' [{}]'.format(p[0])
                        else:
                            p_str += ' <{}>'.format(p[0])
                    d += '`{}{}{}`\n'.format(ctx.prefix, cmd_name, p_str)
                else:
                    d += '`{}{} '.format(ctx.prefix, cmd.name)
                    if cmd.invoke_without_command:
                        d += '['
                    else:
                        d += '<'
                    d += '|'.join(cmd.all_commands.keys())
                    if cmd.invoke_without_command:
                        d += ']`\n'
                    else:
                        d += '>`\n'

                d += '\n**Description:**\n'
                d += '{}\n'.format('None' if cmd.help is None else cmd.help.strip())

                if cmd.aliases:
                    d += '\n**Aliases:**'
                    for alias in cmd.aliases:
                        d += '\n`{}{}`'.format(ctx.prefix, alias)

                    d += '\n'
            '''
            d = '**TWOWBot help:**'

            for i in args:
                if i in ctx.bot.all_commands:
                    cmd = ctx.bot.all_commands[i]
                    d += '\n`{}{}`'.format(ctx.prefix, i)

                    brief = cmd.brief
                    if brief is None and cmd.help is not None:
                        brief = cmd.help.split('\n')[0]

                    if brief is None:
                        brief = 'No description'

                    d += ' - {}'.format(brief)
                else:
                    d += '\n`{}{}` - Command not found'.format(ctx.prefix, i.replace('@', '@\u200b').replace('`', '`\u200b'))
            '''
        d += '\n*Made by @Kenny_#2763*'
        await ctx.send(d)

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Core(bot))