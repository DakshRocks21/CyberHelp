import json
from discord.ext import commands
import discord
import random
import time

from ..utils import database

config = json.load(open("data/config.json"))
SupportLink = config["support"]
InviteLink = config["invite"]
userData = "data/users.json"
featureConfig = "data/featuresConfig.json"

class Currency(commands.Cog):
    """Play with CyberCoins"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False

    @commands.command(description = "Start your Journey", help = "start")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def start(self, ctx):
        data = json.load(open(userData))
        id = ctx.author.id
        name = ctx.author.name
        try:
            x = data[str(id)]
            await ctx.reply("You already have an account")
        except KeyError:
            y = {"name": f"{name}","userid": f"{id}","wallet": 0,"xp": 0,"inv": [],"last mined" : time.time(),"rankNo" : 0,"rank": "Newbie","last daily": time.time()}
            data[str(id)] = y
            print(data)
            with open(userData, "w") as f:
                json.dump(data, f, indent=4)
            embed = discord.Embed(title = "Profile Created", description = f"**{ctx.author.name}** you have created your account\nYou can start earning `XP`\n\n[Invite Me]({InviteLink}) | [Support Server]({SupportLink}) | [Vote For Me](https://top.gg/bot/875229879505911939/vote)",color = 0x2ecc71)
            embed.set_author(name = self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.reply(embed = embed)

    @commands.command(description = "Get CyberCoins by mining", help = "mine")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def mine(self, ctx):
        data = json.load(open(userData))
        id = ctx.author.id
        try:
            x = data[str(id)]
        except KeyError:
            await ctx.send(f":x: **{ctx.author.name}** you need to create a profile before you can do this!\nCreate a profile using `.start`")
            return
        last_mined = float(data[str(id)]["last mined"])
        timeNow = time.time()
        add = int(timeNow - last_mined)
        if add > 9999:
            add = 5000
        totalCoins = data[str(id)]["wallet"] + add
        data[str(id)]["wallet"] = totalCoins
        data[str(id)]["last mined"] = time.time()
        with open(userData, "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title = "Mined", description = f"You earned `{add}`. **Total CyberCoins = `{totalCoins}`**\n\n[Invite Me]({InviteLink}) | [Support Server]({SupportLink}) | [Vote For Me](https://top.gg/bot/875229879505911939/vote)",color = 0x2ecc71)
        embed.set_author(name = ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed = embed)

    @commands.command(description = "Upgrade your Rank", help = "upgrade")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def upgrade(self, ctx):
        data = json.load(open(userData))
        featureData = json.load(open(featureConfig))
        id = ctx.author.id
        try:
            x = data[str(id)]
        except KeyError:
            await ctx.send(f":x: **{ctx.author.name}** you need to create a profile before you can do this!\nCreate a profile using `.start`")
            return
        currentRank = data[str(id)]["rank"]
        currentXp = data[str(id)]["xp"]
        for x in range(len(featureData["currency"]["ranks"])):
            sysRank = featureData["currency"]["ranks"][x]
            if currentRank == sysRank:
                foundRankAt = x
                break
        if currentXp < featureData["currency"]["xpToUpgrade"][foundRankAt]:
            await ctx.send(f'You cannot upgrade yet. Current Xp = {currentXp}/{featureData["currency"]["xpToUpgrade"][foundRankAt]}')
        elif currentXp >= featureData["currency"]["xpToUpgrade"][foundRankAt]:
            newRank = featureData["currency"]["ranks"][foundRankAt + 1]
            embed = discord.Embed(title = "Upgrade", description = f"Leveling up now.\nYour Previous Rank was `{currentRank}`. **Now you are `{newRank}`**\n\n[Invite Me]({InviteLink}) | [Support Server]({SupportLink}) | [Vote For Me](https://top.gg/bot/875229879505911939/vote)",color = 0x2ecc71)
            embed.set_author(name = ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed = embed)
            data[str(id)]["xp"] = currentXp - featureData["currency"]["xpToUpgrade"][foundRankAt]
            data[str(id)]["rank"] = newRank
            data[str(id)]["rankNo"] = data[str(id)]["rankNo"] + 1
            with open(userData, "w") as f:
                json.dump(data, f, indent=4)

    @commands.command(description = "Get your profile", help = "profile <user>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, member : discord.Member=None):
        data = json.load(open(userData))
        if member == None: 
            id = ctx.author.id
        else:
            id = member.id
        try:
            x = data[str(id)]
        except KeyError:
            await ctx.send(f":x: **{ctx.author.name}** Account not found.")
            return
        userName = data[str(id)]["name"]
        userXp = data[str(id)]["xp"]
        userRank = data[str(id)]["rank"]
        userInv = data[str(id)]["inv"]
        userCoins = data[str(id)]["wallet"]
        embed=discord.Embed(title=f"{userName}'s Profile", color=ctx.author.color)
        if member == None: 
            embed.set_thumbnail(url=ctx.author.avatar_url)
        else:
            embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f"Coins: {userCoins}", value = "~~~~", inline=False)
        embed.add_field(name=f"XP: {userXp}", value = "~~~~",inline=False)
        embed.add_field(name=f"Rank: {userRank}", value = "~~~~", inline=False)
        embed.add_field(name=f"Inv: {userInv}", value = "~~~~", inline=False)
        await ctx.send(embed=embed) 

    @commands.command(description = "Coming Soon", help = "shop")
    async def shop(self, ctx):
        await ctx.send("Coming Soon")

    @commands.command(description = "Get Daily coins", help = "daily")
    async def daily(self, ctx):
        data = json.load(open(userData))
        featureData = json.load(open(featureConfig))
        id = ctx.author.id
        try:
            x = data[str(id)]
        except KeyError:
            await ctx.send(f":x: **{ctx.author.name}** you need to create a profile before you can do this!\nCreate a profile using `.start`")
            return
        lastDaily = float(data[str(id)]["last daily"])
        timeNow = time.time()
        checkTime = timeNow - lastDaily
        if checkTime >= 86400:
            currentCoins = data[str(id)]["wallet"]
            dailyCoins = featureData["currency"]["daily"]
            totalCoins = dailyCoins + currentCoins
            data[str(id)]["coins"] = totalCoins
            data[str(id)]["last daily"] = time.time()
            embed = discord.Embed(title = "Daily", description = f"`{dailyCoins}` CyberCoins added into your balance\n\n[Invite Me]({InviteLink}) | [Support Server]({SupportLink}) | [Vote For Me](https://top.gg/bot/875229879505911939/vote)",color = 0x2ecc71)
            embed.set_author(name = ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed = embed)
            with open(userData, "w") as f:
                json.dump(data, f, indent=4)
        else:
            error = 86400 - checkTime
            hours, remainder = divmod(error, 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            embed = discord.Embed(title=f"Command on Cooldown",description = f"This command is on cooldown. \nTry again in {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds", color=0xe74c3c)
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed =embed)


    @commands.group(description = "Leaderboard stats", help = "leaderboard", aliases = ['lb'])
    async def leaderboard(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("The possible options are `coins` and `xp`")

    @leaderboard.command(hidden = True, aliases = ['c'])
    async def coins(self, ctx):
        data = json.load(open(userData))
        leaderboards = []
        for key, value in data.items():
            leaderboards.append(value)
        top = sorted(leaderboards, key=lambda x: x["wallet"], reverse=True)
        embed = discord.Embed(title = "Top 10 Users", description = "In terms of Money",color=discord.Colour.random())
        for i in range(len(top)-1):
            embed.add_field(name = f"{i+1}: {top[i]['name']}", value = f"{top[i]['wallet']} CyberCoins", inline = True)
            if i == 9:
                break
        embed.set_author(name = self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed = embed)

    @leaderboard.command(hidden = True)
    async def xp(self, ctx):
        data = json.load(open(userData))
        leaderboards = []
        for key, value in data.items():
            leaderboards.append(value)
        top = sorted(leaderboards, key=lambda x: x["xp"], reverse=True)
        embed = discord.Embed(title = "Top 10 Users", description = "In terms of XP",color=discord.Colour.random())
        for i in range(len(top)-1):
            embed.add_field(name = f"{i+1}: {top[i]['name']}", value = f"XP: {top[i]['xp']}", inline = True)
            if i == 9:
                break
        embed.set_author(name = self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed = embed)


        
def setup(bot):
    bot.add_cog(Currency(bot))
