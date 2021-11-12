from datetime import datetime
from discord.ext import commands

import discord

class Suggestions(commands.Cog):
    """Request/Report"""
        
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        
    @commands.command(description = "Request a feature", help = "request <feature>")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def request(self, ctx, *, feature):
        channel = self.bot.get_channel(891147396006940692)
        authors_name = str(ctx.author)
        em = discord.Embed(
            title="Feature Request",
            description = f"Name: `{authors_name}`\nFeature: \n{feature}",
            color=0x2ecc71)
        em.set_footer(text = f"Time: `{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}`")
        msg = await channel.send(embed=em)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await ctx.send(f''':pencil: Thanks, "{feature}" has been requested!''')
        await ctx.message.add_reaction('📝')


    @commands.command(description = "Report a command/user", help = "report <`cmd`/`user`>")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def report(self,ctx, *, error_report):
        channel = self.bot.get_channel(904978549746839612)
        authors_name = str(ctx.author)
        em = discord.Embed(
            title="Bug Report",
            description = f"Name: `{authors_name}`\nBug: \n{error_report}",
            color=0xe74c3c)
        em.set_footer(text = f"Time: `{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}`")
        msg = await channel.send(embed=em)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await ctx.send(f''':triangular_flag_on_post: Thanks for the help, "{error_report}" has been reported!''')
        await ctx.message.add_reaction('🚩')


def setup(bot):
    bot.add_cog(Suggestions(bot))
