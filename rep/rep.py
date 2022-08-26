from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import re
import logging


class rep(commands.Cog):
    """
    Reputation cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.log = logging.getLogger('red.tpun.rep')
        self.config = Config.get_conf(
            self,
            identifier=365398642334498816
        )
        default_global = {
            "reputation": {}
        }
        self.config.register_global(**default_global)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if bool(re.search("thank", message.content, flags=re.I | re.X)) and message.mentions is not None:
            users = message.mentions
            names = []
            found: bool = False
            for user in users:
                names.append(user.mention)
            x = await self.config.reputation()
            for user in users:
                id = user.id
                for userId, userRep in x.items():
                    if user.id != message.author.id and userId == str(id):
                        currentRep = userRep + 1
                        newWrite = {id: currentRep}
                        await message.channel.send("**+rep** {0} you now have: {1} Rep".format(user.name, str(currentRep)))
                        found = True
                        break
                if not found:
                    newWrite = {id: 1}
                    await message.channel.send("**+rep** {0} you now have: {1} Rep".format(user.name, str(1)))
                x.pop(str(id), None)
                x.update(newWrite)
            await self.config.reputation.set(x)

    @commands.mod()
    @commands.command(name="repremove")
    async def repremove(self, ctx: commands.Context, user: discord.Member, amount: int):
        """
        Removes a amount from a users reputation
        """
        newWrite = None
        x = await self.config.reputation()
        for userId, userRep in x.items():
            if userId == str(user.id):
                currentRep = userRep - amount
                newWrite = {user.id: currentRep}
                await ctx.send("**-rep** {0} took away {1} rep from {2}. They now have {3}"
                    .format(ctx.author.name, amount, user.name, currentRep)
                )
        if newWrite is not None:
            x.pop(str(user.id), None)
            x.update(newWrite)
        else:
            await ctx.send("This user already has no reputation")
        await self.config.reputation.set(x)

    @commands.command(name="checkrep")
    async def checkrep(self, ctx: commands.Context, user: discord.Member):
        """
        Displays a user's reputation
        """
        userFound = False
        x = await self.config.reputation()
        for userId, userRep in x.items():
            if userId == str(user.id):
                await ctx.send("{0} has {1} reputation".format(user.name, userRep))
                userFound = True
        if userFound is False:
            await ctx.send("{0} doesn't have a reputation.".format(user.name))
