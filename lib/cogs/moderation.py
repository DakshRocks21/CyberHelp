import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """Moderate your Servers"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        
    @commands.command(description = "BROKEN: Add/Remove Roles", help = "role <user> <role>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True) #permissions
    async def role(self, ctx, user : discord.Member, role : discord.Role):
        if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
            return await ctx.send('**:x: | That role is above your top role!**') 
        elif role in user.roles:
            await user.remove_roles(role) #removes the role if user already has
            await ctx.send(f"Removed {role} from {user.mention}")
        else:
            await user.add_roles(role) #adds role if not already has it
            await ctx.send(f"Added {role} to {user.mention}") 

    @commands.command(description ="Delete Messages", help = "purge <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def purge(self, ctx, amount):
        amount = int(amount)
        await ctx.channel.purge(limit=amount+1)

    @commands.command(description = "Kick a Person from your server", help = "kick <user> <user>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)  
    async def kick(self, ctx, member: discord.Member, *, reason):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot kick yourself")
            return
        elif reason == None:
            await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
        await discord.Member.kick(member)
        em = discord.Embed(title = "Kick Hammer", description = "The :foot: :hammer: was used on " + str(member) + " by " + ctx.author.name + ". The reason was  `" + reason + "`", color = ctx.author.color)
        await member.send(embed =em)
        await ctx.send(embed=em)
        

    @commands.command(description = "Lock a channel", help = "lock")
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        em = discord.Embed(title = "Channel Locked", description = ":lock: This channel has been locked" , color = 0xe74c3c)
        await ctx.send(embed=em)

    @commands.command(description = "Unlock a channel", help = "unlock")
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        em = discord.Embed(title = "Channel Unlocked", description = ":unlock: This channel has been unlocked" , color = 0x2ecc71)
        await ctx.send(embed=em)

    @commands.command(description = "Ban Members", help = "ban <user> <reason>")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        if member == None or member == ctx.author:
            await ctx.channel.send("You cannot ban yourself")
            return
        elif reason == None:
            await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
            return
        else:
            await ctx.guild.ban(user=member, reason=reason)
            em = discord.Embed(title = "Ban Hammer", description = "The **BAN** :hammer: was used on " + str(member) + " by " + ctx.author.name + ". The reason was  `" + reason + "`", color = ctx.author.color)
            await member.send(embed = em)
            await ctx.send(embed = em)

    @commands.command(description = "Unbans a Member", help = "unban <user> <reason>")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unban(self, ctx, member = None,*, reason = None):
        if member == None:
            await ctx.send("Pls provide at UserId")
        if reason == None:
            reason = "No reason was provided"
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)
        em = discord.Embed(title = "UNBan Hammer", description = "The **UNBAN** :hammer: was used on " + str(member) + " by " + ctx.author.name + f". Reason was `{reason}`", color = ctx.author.color)
        await member.send(embed = em)
        await ctx.send(embed = em)

    @commands.command(description = "SoftBan Members", help = "softban")
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def softban(self, ctx, *, member : discord.Member):
        reason = "Softban used by" + ctx.author.name
        await ctx.guild.ban(user=member, reason=reason)
        await ctx.guild.unban(user=member, reason=reason)
        em = discord.Embed(title = f"Softban on {member.name}", description = str(member) + " was Softbanned by " + ctx.author.name, color = ctx.author.color)
        await member.send(embed = em)
        await ctx.send(embed = em)

    @commands.command(description = "Set Slowmode", help = "Slowmode")
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")



def setup(bot):
    bot.add_cog(Moderation(bot))
"""
    @commands.command() 
    @commands.guild_only() 
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True) 
    async def createcategory (self, ctx, role: discord. Role, name): 
        overwrites = { 
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), ctx.guild.me: discord.PermissionOverwrite(read_messages=True), 
            role: discord.Permission0verwrite(read_messages=True) 
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites) 
        await ctx.send(f"Hey dude, I made {category.name} for ya!")

"""