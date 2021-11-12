import os
import discord
from discord.ext import commands
import json
import data.blacklist as bad_things
from lib.utils.webserver import keep_alive
from datetime import datetime

os.system("pip install PyNaCl")
os.system("pip install buttons")
#os.system("python -m pip install -U git+https://github.com/Rapptz/discord-ext-menus")
TOKEN = os.environ['TOKEN']
botPrefix = [".", ">"]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=botPrefix, case_insensitive=True, intents=intents)
#bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned or botPrefix, case_insensitive=True, intents=intents)
############################
#         on_ready         #
############################    

@bot.event
async def on_ready():
    bot.launch_time = datetime.utcnow()
    for guild in bot.guilds:
        print("- " + str({guild.id}) + " Name: " + str({guild.name}))

    print(str(bot.user) + " is in " + str(len(bot.guilds)) + " guilds.\n \n ")
    await bot.change_presence(
        activity=discord.Activity(name=f" .help on {len(bot.guilds)} server's",
                                  type=discord.ActivityType.watching))


##########################
#        botLoops        #
##########################
import random
import asyncio

#async def musicPyNaCl():
#    await bot.wait_until_ready()

#    while not bot.is_closed():
#        os.system("pip install PyNaCl")
#        bot.reload_extention("music")
#        await asyncio.sleep(10800)
        
#bot.loop.create_task(musicPyNaCl())

async def statusLoop():
    await bot.wait_until_ready()
    arr = [
        f" .help on {len(bot.guilds)} server's",
        f" >help on {len(bot.guilds)} server's", " the latest Cyber News"
    ]

    while not bot.is_closed():
        status = random.choice(arr)
        await bot.change_presence(activity=discord.Activity(
            name=status, type=discord.ActivityType.watching))
        await asyncio.sleep(5)


bot.loop.create_task(statusLoop())

#############################
#        on_message         #
#############################


@bot.event
async def on_message(ctx):
    z = json.load(open("data/config.json"))
    beta = z["beta"] 

    if isinstance(ctx.channel, discord.DMChannel):
        return
    if ctx.author.bot:
        return
    if ctx.content.strip() == f"<@!{bot.user.id}>":
        await ctx.channel.send(f"My prefix is `{botPrefix[0]}`")

    if any(blacklist in str(ctx.author.id) for blacklist in bad_things.blacklist_id):
        await ctx.channel.send(
            "Bad Luck, " + ctx.author.mention +
            ", You are currently blacklisited. Please message in #help in my Community Server. "
        )
        return await ctx.delete()
    
    if beta == "0" or ctx.author.id == z["owner_id"][0]:
        await bot.process_commands(ctx)
    else: 
        if ctx.content.startswith('.') or ctx.content.startswith('>'):
            await ctx.channel.send("Bot is in Develpment Mode. Try again later")
        else:
            return

for file in os.listdir("lib/cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"lib.cogs.{name}")

keep_alive()
bot.run(TOKEN)
