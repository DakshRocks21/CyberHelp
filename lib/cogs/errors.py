import discord
from discord.ext import commands
import traceback


class Errors(commands.Cog):
    """Error Handling"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, bypass=False):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Unauthorised Access",
                description="You are not authorised to use this command.",
                colour=0xe74c3c,
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions",
                description="You do not have permission to run this command.",
                colour=0xe74c3c,
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions",
                description="CyberHelp does not have permission to run this command.",
                colour=0xe74c3c,
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            z = round(error.retry_after)
            embed = discord.Embed(
                title="Command on Cooldown",
                description=f"This command is on cooldown. Try again in {error.retry_after:,.1f} seconds.",
                colour=0xe74c3c,
            )
            hours, remainder = divmod(z, 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            embed = discord.Embed(title=f"Command on Cooldown",description = f"This command is on cooldown. \nTry again in {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds", color=0xe74c3c)

            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Incorrect Argument",
                description=f"There is an error with your command statement. Please check your command syntax through `.help {ctx.invoked_with}`.",
                colour=0xe74c3c,
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.channel.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Missing required argument",
                description=f"You are missing required arguments. Please check your command syntax through `.help {ctx.invoked_with}`.",
                colour=0xe74c3c,
            )

            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(
                title="Guild Only",
                description=f"`{ctx.invoked_with}` cannot be used in DM channels",
                colour=0xe74c3c,
            )

            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                title="Disabled Command",
                description=f"`{ctx.invoked_with}` is Disabled",
                colour=0xe74c3c,
            )

            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Unknown Error",
                description=f"An error occurred: ```py\n{str(error)}```",
                colour=0xe74c3c,
            )
            embed.set_footer(text = "You may use the report command")
            await ctx.send(embed = embed)
            raise error


def setup(bot):
    bot.add_cog(Errors(bot))
