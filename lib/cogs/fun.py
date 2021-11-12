from datetime import datetime
import asyncio
import requests
import json
import discord
from discord.ext import commands
import random
import pyfiglet



class Fun(commands.Cog):
    """Have Fun with your friends"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False


    @commands.command(name = 'eject',description = "eject somone", help = "eject <member>", pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eject(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("Are you trying to self eject???")
            return
        crew = ["black", "blue", "brown", "cyan", "darkgreen", "lime", "orange", "pink", "purple", "red", "white", "yellow"]
        imposter = ["true", "false"]
        embed = discord.Embed(title = f"{ctx.author.name} decided to eject ${member.name}", color=discord.Colour.random())
        embed.set_image(url = f"https://vacefron.nl/api/ejected?name={member.name}&impostor={random.choice(imposter)}&crewmate={random.choice(crew)}")
        await ctx.send(embed = embed)

    @commands.command(name = 'water',description = "water image", help = "water <text>", pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def water(self, ctx,*,text):
        text = text.replace(" ", "%20")
        embed = discord.Embed(title = f"{ctx.author.name} used water")
        embed.set_image(url = f"https://vacefron.nl/api/water?text={text}")
        await ctx.send(embed = embed)

    @commands.command(name = 'digital',description = "Get digital text", help = "digital", pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def digital(self, ctx, *, text):
        result = pyfiglet.figlet_format(text, font = "digital")
        await ctx.reply(f"```{result}```")

    @commands.command(name = 'slant',description = "Get slant text", help = "slant", pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slant(self, ctx, *, text):
        result = pyfiglet.figlet_format(text, font = "slant")
        await ctx.reply(f"```{result}```")

    @commands.command(name = 'ascii',description = "Get ascii text", help = "ascii", pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ascii(self, ctx, *, text):
        result = pyfiglet.figlet_format(text)
        await ctx.reply(f"```{result}```")

    @commands.command(name = 'quote',description = "Get a Quote", help = "quote", aliases = ['q'], pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def quote(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        embed = discord.Embed(title = "Quote", description = f"```{quote}```",color=discord.Colour.random())
        embed.set_footer(text = f"Requested by {ctx.author.name}")
        await ctx.reply(embed = embed)

    @commands.command(name = 'bitcoin', description = "Gives Current Bitcoin Value", help = "bitcoin", aliases = ['btc'], pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bitcoin(self, ctx):
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        response = requests.get(url)
        value = response.json() ['bpi'] ['USD'] ['rate']
        embed = discord.Embed(title = "Bitcoin Prices", description = "```Bitcoin prices is: **US$" + value + "**```",color=discord.Colour.random())
        embed.set_footer(text = f"Requested by {ctx.author.name}")
        await ctx.reply(embed = embed)
        await ctx.message.add_reaction('🪙')

    @commands.command(name = '8Ball', description = "Let the 8 Ball Predict Your Life choices for you!", help = "8ball <question>", aliases = ['eightball'], pass_context = True) 
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eightball(self, ctx, *, question): 
        responses = [
            "idk im not jesus", 
            ("why dont u ask someone else ," + ctx.author.mention),
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        response = random.choice(responses)
        embed=discord.Embed(title="The Magic 8 Ball has Spoken!",color=discord.Colour.random())
        embed.add_field(name='Question: ', value = question, inline=True)
        embed.add_field(name='Answer: ', value=f'{response}', inline=False)
        embed.set_footer(text = f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('🎱')


    @commands.command(description = "Google Something", help = "google <string>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self,ctx, *, query):
        query = query.replace(" ", "%20")
        url = "https://www.google.com/search?q=" + query
        await ctx.send("**Here's the link: " + url + "**")

    @commands.command(description = "Get a coinfilp", aliases = ["coin", "cointoss", "filp"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinfilp(self,ctx):
        coin = random.randint(0,1)
        if coin == 0:
            await ctx.reply("You got **HEADS**")
        else:
            await ctx.reply("You got **TAILS**")

    @commands.command(description = "Role a Dice", help = "dice <sides> ")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dice(self,ctx, limit = None):
        if limit == None:
            up = 6
        else:
            limit = int(limit)
            up = limit
        coin = random.randint(1,up)
        await ctx.reply(f"Rolled Number: {coin}\nRolled from 1 to {up}")

    @commands.command(description = "Get Memes",help = "meme", aliases=["m"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        
        response = requests.get("https://meme-api.herokuapp.com/gimme").json()
        embed = discord.Embed(
            title=response["title"],
            description="SubReddit = `r/{0}`\nPublisher: `{1}`".format(
                response["subreddit"], response["author"]),
            color=discord.Colour.random())
        embed.set_image(url=response["url"])
        upvotes = response["ups"]
        embed.set_footer(text = f"Upvotes: {upvotes}\nRequested by: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(aliases = ["emoji"], description = "Emojify text", help = "emojify <string>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        emojis = []
        text = text.lower()
        for items in text:
            if items.isdecimal():
                numword = {"0": "zero", "1" : "one", "2" : "two","3" : "three","4" : "four","5" : "five","6" : "six","7" : "seven","8" : "eight","9" : "nine"}
                emojis.append(f":{numword.get(items)}:")
            elif items.isalpha():
                emojis.append(f":regional_indicator_{items}:")
            else:
                emojis.append(items)
        await ctx.send("".join(emojis))
                
    @commands.command(description = "Get a Joke", help = "joke")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joke(self, ctx):
        response = requests.get("https://v2.jokeapi.dev/joke/any?blacklistFlags=nsfw,religious,sexist,explicit").json()
        if response["type"] == "single":
            embed = discord.Embed(title = f'{response["category"]} Joke', description = f"```{response['joke']}```", color=discord.Colour.random())
        if response["type"] == "twopart":
            embed = discord.Embed(title = f"{response['category']} Joke", description = f'```{response["setup"]}\n\n{response["delivery"]}```', color=discord.Colour.random())
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Fun(bot))
