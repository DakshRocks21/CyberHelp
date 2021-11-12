import json
import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import time
import requests

config = json.load(open("data/config.json"))
SupportLink = config["support"]
InviteLink = config["invite"]

class Utility(commands.Cog):
    """Misc Commands"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False

    @commands.command(description = "Get Cmds Stats")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, ctx):
        data = json.load(open("data/cmdData.json"))
        leaderboards = []
        for key, value in data.items():
            leaderboards.append(value)
        top = sorted(leaderboards, key=lambda x: x["usage"], reverse=True)
        embed = discord.Embed(title = "Top 10 Commands",color=discord.Colour.random())
        for i in range(len(top)-1):
            embed.add_field(name = f"{i+1}: {top[i]['name']}", value = f"{top[i]['usage']} times", inline = True)
            if i == 9:
                break
        embed.set_author(name = self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(description = "Get the bot's uptime", help = "uptime")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        e = discord.Embed(title=f"Uptime",description = f"I am Online for {days} days, {hours} hours, {minutes} minutes, {seconds} seconds", color=discord.Color.green())
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        e.set_thumbnail(url=self.bot.user.avatar_url)
        e.set_footer(text = f"Requested by {ctx.author}")
        await ctx.send(embed=e)

    @commands.command(aliases = ["grepo"], description = "Get the top treading github repos", help = "github")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def githubrepo(self,ctx ):
        amount = 10
        msg = await ctx.reply("Loading. Please give me a momment")
        embed = discord.Embed(title = f"Top {amount} Github Repos",color=discord.Colour.random())
        for id in range(amount):
            author = requests.get("https://api.trending-github.com/github/repositories").json()[id]["author"]
            name = requests.get("https://api.trending-github.com/github/repositories").json()[id]["name"]
            description = requests.get("https://api.trending-github.com/github/repositories").json()[id]["description"]
            url = requests.get("https://api.trending-github.com/github/repositories").json()[id]["url"]
            embed.add_field(name = f"Treading #{id+1}: {name}" , value = f"{description}\n[Link]({url})\nAuthor: `{author}`", inline = False)
            id = id + 1
        embed.set_footer(text = f"Requested by: {ctx.author}")
        await msg.reply(embed = embed)

    @commands.command(aliases = ["info"], description = "Get a User's Info/Permissons", help = "userinfo <user>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, member : discord.Member=None):
        mention = []
        if not member:
            member = ctx.message.author
        for role in member.roles:
            if role.name != "@everyone":
                mention.append(role.mention)
        b = ", ".join(mention)
        em = discord.Embed(title=f" ", color=discord.Colour.random())
        em.set_author(name=member.name, icon_url=member.avatar_url)
        em.add_field(name="ID", value=member.id, inline=True)
        em.add_field(name="Top Role:", value=member.top_role.mention, inline=True)
        em.add_field(name="Roles:", value=b, inline = False)
        em.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        em.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = True)
        arr = []
        for perm, ele in iter(member.guild_permissions):
            if ele:
                arr.append(perm)
        em.add_field(name="Permissions in Guild :", value=arr, inline = False)
        arr= []
        for perm, ele in iter(member.permissions_in(ctx.channel)):
            if ele:
                arr.append(perm)
        em.add_field(name="Permissions in Channel:", value=arr, inline = True)
        em.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed = em)

    @commands.command(name = 'serverInfo', aliases = ['server', 'aboutServer'], pass_context = True, description = "Get server Info", help = "serverinfo")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def where_am_i(self, ctx):
        owner= str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        desc=str(ctx.guild.description)
        # threads = len(ctx.guild.threads) 
        # active_threads =  len(await ctx.guild.active_threads()) 
        voice_channels = len(ctx.guild.voice_channels) 
        stages = len(ctx.guild.stage_channels) 
        text_channels = len(ctx.guild.text_channels)

        embed = discord.Embed(
            title=ctx.guild.name + " Server Information",
            description=desc,
            color=discord.Colour.random()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=True)
        embed.add_field(name='Roles', value=len(ctx.guild.roles), inline=True)
        # embed.add_field(name='Threads', value=threads, inline=True)
        # embed.add_field(name='Active Threads', value=active_threads, inline=True)
        embed.add_field(name='Voice Channels', value=voice_channels, inline=True)
        embed.add_field(name='Stages', value=stages, inline=True)
        embed.add_field(name='Text Channels', value=text_channels, inline=True)

        await ctx.send(embed=embed)
        await ctx.message.add_reaction('ℹ️')

    @commands.command(name = 'ping', description = "Get the ping for me", help = "ping")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.send(f":white_check_mark: - Ping : {round(self.bot.latency * 1000)}ms!")
        end_time = time.time()
        await message.edit(content=f":white_check_mark: - Ping : {round(self.bot.latency * 1000)}ms!\nAPI: {round((end_time - start_time) * 1000)}ms")
        await ctx.message.add_reaction('🏓')
        
    @commands.command(name = 'invite', description = "Get the invite link of the bot", help = "invite")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        em = discord.Embed(title = "Thanks for using the bot", color=discord.Colour.random())
        em.add_field(name = "Invite Me", value = f"[Click Me]({InviteLink})", inline=True) 
        em.add_field (name = "Support Server", value = f"[Click Me]({SupportLink})", inline=True) 
        em.set_footer(text=f"Owner: DakshRocks21#4167")
        await ctx.send(embed=em)
    @commands.command(aliases = ["remind", "remindme", "remind_me"], description = "Set a reminder", help = "reminder")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def reminder(self, ctx, time, *, reminder):
        user = ctx.author.mention
        embed = discord.Embed(color=discord.Colour.random(), timestamp=datetime.utcnow())
        seconds = 0
        
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what I should remind you about.') # Error message
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s") or time.lower().endswith("seconds"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"
        if seconds <= 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration')
            await ctx.send(embed=embed)
        elif seconds < 300:
            embed.add_field(name='Warning',
                            value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
            await ctx.send(embed=embed)
        elif seconds > 7776000:
            embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
            await ctx.send(embed=embed)
        else:
            embed.add_field(name = "Reminder Set", value = f"Alright, I will remind you about `{reminder}` in `{counter}`.", 
            inline=False )
            if seconds > 86400:
                embed.set_footer(text='This bot is in Dev Mode. This means it gets updated almost every 1 - 2 days. When I mean updated it restarts and removes your reminders.')
            await ctx.send(embed=embed)
            await asyncio.sleep(seconds)
            
            await ctx.author.send(f"Hi {user}, you asked me to remind you about `{reminder}` `{counter}` ago.")
            await ctx.send(f"Hi {user}, you asked me to remind you about `{reminder}` `{counter}` ago.")
            return
            
    @commands.command(description = "Vote for CyberHelp", help = "vote")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def vote(self,ctx):
        em = discord.Embed(title="Vote for CyberHelp",description = f"**{ctx.author.name}**  please vote for me!",color = 0x2ecc71)
        em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        em.set_thumbnail(url=ctx.author.avatar_url)
        em.add_field(name="Top.gg", value="https://top.gg/bot/875229879505911939/vote", inline=False)
        em.add_field(name="Discord Bot List:", value="https://discords.com/bots/bot/875229879505911939/vote", inline=True)
        em.set_footer(text = "Thank you for Voting")
        await ctx.send(embed = em)
    @commands.command(description = "Show's bot info", help = "botinfo")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def botinfo(self, ctx):
        botdata = json.load(open("data/config.json"))
        sumCMD = 0
        for i in self.bot.cogs:
            for x in self.bot.get_cog(i).walk_commands():
                sumCMD = sumCMD + 1

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        text_channel_list = []
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                text_channel_list.append(channel)
        voice_channel_list = []
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                voice_channel_list.append(channel)
        em = discord.Embed(description = f"Developers: DakshRocks21#4167 & P3RPL3X#0878", color=discord.Colour.random())
        em.set_thumbnail(url=ctx.author.avatar_url)
        em.add_field(name="❯ Uptime", value= f"{uptime}", inline=True)
        em.add_field(name="❯ WebSocket Ping", value= f"{round(self.bot.latency * 1000)}ms", inline=True)
        em.add_field(name="❯ Guild Count", value= f"{str(len(self.bot.guilds))} guilds", inline=True)
        em.add_field(name="❯ Users Count", value= f"{len(self.bot.users)} use me", inline=True)
        em.add_field(name="❯ Commands", value= f"{sumCMD} cmds", inline=True)
        em.add_field(name="Text Channels", value=len(text_channel_list), inline=True)
        em.add_field(name="Voice Channels", value=len(voice_channel_list), inline=True)
        em.add_field(name="❯ Invite Link", value= f"[Click Me](https://discord.com/api/oauth2/authorize?client_id=875229879505911939&permissions=8&scope=bot%20applications.commands) ", inline=True)
        em.add_field(name="❯ Support Server", value= f"[Paragon Official Server]({SupportLink}) ", inline=True)
        em.add_field(name="❯ Vote Link", value= f"[Top.gg](https://top.gg/bot/875229879505911939/vote)", inline=True)
        em.set_author(name = f"CyberHelp {botdata['version']}", icon_url=self.bot.user.avatar_url)
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_footer(text = f"Requested by {ctx.author}")
        await ctx.send(embed = em)

    @commands.command(description = "Get Github Stats for a User", help = "github <user>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def github(self, ctx, *, user):
        try:
            response = requests.get("https://api.github.com/users/" + user)
            x = json.loads(response.text)
            name = x["login"]
            id = x["id"]
            bio = x["bio"]
            pic = x["avatar_url"]
            url = x["html_url"]
            compan = x["company"]
            location = x["location"]
            email = x["email"]
            follower = x["followers"]
            following = x["following"]
            repo = x["public_repos"]
            embed = discord.Embed(title = f"{name} ({id})", description = f"{bio}", color=discord.Colour.random())
            embed.add_field(name =f"Followers", value = f"```{follower}```", inline = True)
            embed.add_field(name =f"Following", value = f"```{following}```", inline = True)
            embed.add_field(name =f"Repositories", value = f"```{repo}```", inline = True)
            embed.add_field(name =f"Email", value = f"```{email}```", inline = False)
            embed.add_field(name =f"Company", value = f"```{compan}```", inline = False)
            embed.add_field(name =f"Location", value = f"```{location}```\n[Github Link]({url})", inline = False)
            embed.set_thumbnail(url = pic)
            await ctx.send(embed = embed)
        except:
            await ctx.reply(f"`{user}` not found")

    @commands.command(description = "Get user's avatar", help = "avatar <user>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author
        em = discord.Embed(title = f"Avatar for {user}")
        em.add_field(name = "Download the Avatar", value = f"[Click Here]({user.avatar_url})")
        em.set_image(url = user.avatar_url)
        await ctx.send(embed = em)

    @commands.command(description = "Get user's avatar", help = "avatar <user>")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def channelstats(self, ctx, channel:discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel. name}**", description = f" {' Category: {}'.format (channel.category.name) if channel.category else 'This channel is not in a category'}", color=discord.Colour.random())
        embed.add_field(name="Guild", value=ctx.guild.name, inline=True)
        embed.add_field(name="Id", value=channel.id, inline=True) 
        embed.add_field(name="Slowmode Delay", value=channel.slowmode_delay, inline=True) 
        embed.add_field(name="Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=True) 
        embed.add_field(name="Creation Time", value=channel.created_at, inline=True) 
        embed.add_field(name="Position", value=channel.position, inline=True) 
        embed.add_field(name="Permissions Synced", value=channel.permissions_synced, inline=True) 
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True) 
        embed.add_field(name="Announcments", value=channel.is_news(), inline=True) 
        embed.add_field(name="Permissions Synced", value=channel.permissions_synced, inline=True) 
        embed.add_field(name="Channel Hash", value=hash(channel), inline=True)
        await ctx.send(embed = embed)



    @commands.command(name="emojiinfo", aliases=["ei"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        if not emoji:
            return await ctx.send("Pls give an emoji")

        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.NotFound:
            return await ctx.send("I could not find this emoji in the given guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = (
            "Everyone"
            if not emoji.roles
            else " ".join(role.name for role in emoji.roles)
        )

        description = f"""
        **General:**
        **- Name:** {emoji.name}
        **- Id:** {emoji.id}
        **- URL:** [Link To Emoji]({emoji.url})
        **- Author:** {emoji.user.mention}
        **- Time Created:** {creation_time}
        **- Usable by:** {can_use_emoji}
        
        **Other:**
        **- Animated:** {is_animated}
        **- Managed:** {is_managed}
        **- Requires Colons:** {requires_colons}
        **- Guild Name:** {emoji.guild.name}
        **- Guild Id:** {emoji.guild.id}
        """

        embed = discord.Embed(
            title=f"**Emoji Information for:** `{emoji.name}`",
            description=description,
            colour=0xADD8E6,
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)
    
    @commands.command(name="createinvite")
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def createinvite(self, ctx):
        invite = await ctx.channel.create_invite()
        await ctx.send(f"**Here's the link: **{invite}")

def setup(bot):
    bot.add_cog(Utility(bot))
