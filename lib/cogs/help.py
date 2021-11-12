import discord
from discord.ext import commands


class Help(commands.Cog):
    """Get Help Here"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        self.bot.remove_command('help') 

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    @commands.command(description='Get help for a Command or Catergory', help = "help")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx, *args):
        embed = discord.Embed()
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        if not args:
            embed.title = 'List of Command Catergories'
            for i in self.bot.cogs:
                if not self.bot.cogs[i].hidden:
                    embed.add_field(name=i, value=f"> {self.bot.cogs[i].__doc__}", inline=True)
        else:
            arg = ' '.join(args)
            found = False
            for i in self.bot.cogs:
                if i == arg:
                    embed.title, embed.description = f'List of Command in {i}', f"> {self.bot.cogs[i].__doc__}"
                    found = True
                for x in self.bot.get_cog(i).walk_commands():
                    if x.hidden:
                        pass
                    elif found:
                        embed.add_field(name=x.name, value=f"> {x.description}", inline=True)
                    elif x.name == arg:
                        embed.title, embed.description = x.name, f"> {x.description}"
                        embed.add_field(name="Syntax", value = f"```{self.get_command_signature(x, ctx)}```", inline = True)
                        await ctx.send(embed=embed)
                        return
                else:
                    if found:
                        break
            if not found:
                embed.title, embed.description, embed.colour = 'Error!', f'"`{arg}` not Found"?', discord.Color.red()
        embed.add_field(name="Additional Help", value = "[Support Server](https://discord.gg/zc2JyyH2DF)", inline = False)
        embed.set_footer(text='Use .help [Catergory]/[command] to find out more about them!\nCatergories start with captial letter. Commands are all lower case. ')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))