from xmlrpc.client import Boolean
from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import json


class rep(commands.Cog):
    """
    Reputation cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )
        global jsonPath
        path = data_manager.cog_data_path(cog_instance=self)
        jsonPath = path / 'reputation.json'
        if jsonPath.exists():
            pass
        else:
            with jsonPath.open("w", encoding="utf-8") as f:
                f.write("{}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        global jsonPath
        if "thank you" in message.content or "thanks" in message.content or "Thank you" in message.content or "THANK YOU" in message.content or "Thank You" in message.content:
            if message.mentions is not None:
                users = message.mentions
                names = []
                newUser: Boolean = True
                for user in users:
                    names.append(user.mention)
                for user in users:
                    if user.id != message.author.id:
                        id = user.id
                        with open(str(jsonPath), 'r') as reputation:
                            print(reputation)
                            try:
                                x = json.load(reputation)
                                for userId, userRep in x.items():
                                    if userId == str(id):
                                        currentRep = userRep + 1
                                        newWrite = {id: currentRep}
                                        await message.channel.send("**+rep** {0} you now have: {1} Rep".format(user.name, str(currentRep)))
                                        newUser = False
                                if newUser:
                                    newWrite = {id : 1}
                                    await message.channel.send("**+rep** {0} you now have: {1} Rep".format(user.name, str(1)))
                                x.pop(str(id), None)
                                x.update(newWrite)
                            except ValueError:
                                if x is None:
                                    x = {}
                        with open(str(jsonPath), 'w') as reputationWrite:
                            try:
                                json.dump(x, reputationWrite)
                            except ValueError:
                                print("reputation.json write failed.")

    @commands.mod()
    @commands.command(name="repremove", help="Removes a amount from a users reputation")
    async def repremove(self, ctx: commands.Context, user: discord.Member, amount:int):
        newWrite = None
        with open(str(jsonPath), 'r') as reputation:
            try:
                x = json.load(reputation)
                for userId, userRep in x.items():
                    if userId == str(user.id):
                        currentRep = userRep - amount
                        newWrite = {user.id : currentRep}
                        await ctx.send("**-rep** {0} took away {1} rep from {2}. They now have {3}".format(ctx.author.name, amount, user.name, currentRep))
                if newWrite is not None:
                    x.pop(str(user.id), None)
                    x.update(newWrite)
                else:
                    await ctx.send("This user already has no reputation")
            except ValueError:
                print("reputation.json failed to read")
        with open(str(jsonPath), 'w') as reputationWrite:
            try:
                json.dump(x, reputationWrite)
            except ValueError:
                print("reputation.json failed to write")

    @commands.command(name="checkrep", help="Displays a user's reputation")
    async def checkrep(self, ctx: commands.Context, user: discord.Member):
        userFound = False
        with open(str(jsonPath), 'r') as reputation:
            try:
                x = json.load(reputation)
                for userId, userRep in x.items():
                    if userId == str(user.id):
                        await ctx.send("{0} has {1} reputation".format(user.name, userRep))
                        userFound = True
            except ValueError:
                print("reputation.json failed to read")
        if userFound is False:
            await ctx.send("{0} doesn't have a reputation.".format(user.name))
