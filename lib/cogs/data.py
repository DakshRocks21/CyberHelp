import discord
from discord.ext import commands
import json
from lib.utils.logger import Logger

logger = Logger()


class listener(commands.Cog):
    """Misc Commands"""
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    @commands.Cog.listener(name='on_command')
    async def onCMD(self, ctx):
        botconfig = json.load(open("data/config.json"))
        logger.config(botconfig["logger"], "CyberHelp")
        data = json.load(open("data/users.json"))
        id = ctx.author.id
        try:
            x = data[str(id)]
        except KeyError:
            await ctx.send(f":x: **{ctx.author.name}** please do `.start`")
            return
        botData = json.load(open("data/config.json"))
        addXp = botData["addXp"]
        currentXp = data[str(id)]["xp"]
        finalXp = addXp + currentXp
        data[str(id)]["xp"] = finalXp
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

        helpData = json.load(open("data/cmdData.json"))
        try:
            if not ctx.command.hidden:
                server = ctx.guild.name
                user = ctx.author
                command2 = ctx.command
                logger.debug(f"{server} > {user} > {command2}")
                logger.info(f"{user}: {command2}")
                x = helpData[ctx.invoked_with]["usage"]
                helpData[ctx.invoked_with]["usage"] = x + 1
            else: pass
        except KeyError:
            helpData[ctx.invoked_with] = {"name": f"{ctx.invoked_with}","usage": 1}
        with open("data/cmdData.json", "w") as f:
            json.dump(helpData, f, indent=4)

def setup(bot):
    bot.add_cog(listener(bot))
