
from discord.ext import commands
import requests
import discord



class Animal(commands.Cog):
    """Get random Facts/Pictures"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False

    @commands.command(description='Get cat Facts/Pictures', help = "cat")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cat(self, ctx):
        response = requests.get("https://some-random-api.ml/animal/cat").json()
        embed = discord.Embed(
            title="Cat Facts/Pictures",
            color=discord.Colour.random())
        embed.set_image(url=response["image"])
        embed.add_field(name = "Fact", value = f"```{response['fact']}```")
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(description='Get dog Facts/Pictures', help = "dog")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dog(self, ctx):
        response = requests.get("https://some-random-api.ml/animal/dog").json()
        embed = discord.Embed(
            title="Dog Facts/Pictures",
            color=discord.Colour.random())
        embed.set_image(url=response["image"])
        embed.add_field(name = "Fact", value = f"```{response['fact']}```")
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(description='Get panda Facts/Pictures', help = "panda")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def panda(self, ctx):
        response = requests.get("https://some-random-api.ml/animal/panda").json()
        embed = discord.Embed(
            title="Panda Facts/Pictures",
            color=discord.Colour.random())
        embed.set_image(url=response["image"])
        embed.add_field(name = "Fact", value = f"```{response['fact']}```")
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(description='Get fox Facts/Pictures', help = "fox")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fox(self, ctx):
        response = requests.get("https://some-random-api.ml/animal/fox").json()
        embed = discord.Embed(
            title="Fox Facts/Facts/Pictures",
            color=discord.Colour.random())
        embed.set_image(url=response["image"])
        embed.add_field(name = "Fact", value = f"```{response['fact']}```")
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(description='Get koala Facts/Pictures', help = "koala")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def koala(self, ctx):
        response = requests.get("https://some-random-api.ml/animal/koala").json()
        embed = discord.Embed(
            title="Koala Facts/Pictures",
            color=discord.Colour.random())
        embed.set_image(url=response["image"])
        embed.add_field(name = "Fact", value = f"```{response['fact']}```")
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(description='Get bird Facts/Pictures', help = "bird")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bird(self, ctx):
        response = requests.get("https://some-random-api.ml/animal/bird").json()
        embed = discord.Embed(
            title="Bird Facts/Pictures",
            color=discord.Colour.random())
        embed.set_image(url=response["image"])
        embed.add_field(name = "Fact", value = f"```{response['fact']}```")
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(description='Get kangaroo Facts/Pictures', help = "kangaroo")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kangaroo(self, ctx):
        response = requests.get("https://some-random-api.ml/animal/kangaroo").json()
        embed = discord.Embed(
            title="Kangaroo Facts/Pictures",
            color=discord.Colour.random())
        embed.set_image(url=response["image"])
        embed.add_field(name = "Fact", value = f"```{response['fact']}```")
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Animal(bot))