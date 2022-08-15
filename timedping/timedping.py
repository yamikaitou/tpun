from multiprocessing.sharedctypes import Value
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import time
import asyncio
from redbot.core import data_manager
import json
import re

global tempo
tempo : dict = {}

class timedping(commands.Cog):
    """
    Timed Ping cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )
        global pingListPath
        path = data_manager.cog_data_path(cog_instance=self)
        pingListPath = path / 'pingList.json'
        if pingListPath.exists():
            pass
        else:
            with pingListPath.open("w", encoding ="utf-8") as f:
                f.write("{}")

    def pingListRead(self, guild: int, roleArg: discord.role):
        global pingListPath
        try:
            with open(str(pingListPath), 'r') as pingList:
                x = json.load(pingList)
                for server, rolesList in x.items():
                    if server == str(guild):
                        for i in rolesList:
                            for role, cooldown in i.items():
                                if role == roleArg.id:
                                    return cooldown
        except ValueError:
            print("pingList.json failed to read")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        global tempo
        guild = message.guild.id
        roles = {}
        notInTempo = True
        if "@" in message.content:
            try:
                with open(str(pingListPath), 'r') as pingList:
                    x = json.load(pingList)
                    for server, rolesList in x.items():
                        if server == str(guild):
                            for i in rolesList:
                                roles = i
            except ValueError:
                print("pingList.json failed to read")
        for role, cooldown in roles.items():
            if bool(re.search(message.guild.get_role(int(role)).name, message.content, flags= re.I | re.X)) or bool(re.search(message.guild.get_role(int(role)).name, message.content, flags= re.I)):
                print("ping found")
                for x, y in tempo.items():
                    print(x)
                    print(y)
                    if x == str(role):
                        notInTempo = False
                        print("role found in tempo")
                        if y > time.time():
                            await message.reply("There is a {0} hour cooldown in between vc ping uses. There is <t:{1}:R> remaining in the cooldown".format(str(cooldown), int(y)))
                        else:
                            await message.reply("<@&{0}}>".format(role))
                            tempo.update(str(role), int(time.time() + cooldown))
                    else:
                        print("role isn't in tempo")
                        notInTempo = True
                if notInTempo:
                    await message.reply("<@&{0}}>".format(int(role)))
                    tempo.update(str(role), int(time.time() + cooldown))

    @commands.guildowner_or_permissions()
    @commands.group(name="tping", help="Base command for all timed ping commands")
    async def tping(self, ctx):
        pass

    @tping.command(name="add", usage=" <role mention> <cooldown>", help="Adds a role to the timed ping list")
    async def add(self, ctx, role: discord.Role, cooldown: int):
        global pingListPath
        guild = ctx.guild.id
        nC = {role.id : cooldown}
        with open(str(pingListPath), 'r') as pingList:
            try:
                x = json.load(pingList)
                if str(guild) in x:
                    y = x[str(guild)].copy()
                    y[0].update(nC)
                else:
                    x.update({str(guild) : [{}]})
                    y = x[str(guild)].copy()
                    y[0].update(nC)
            except ValueError:
                print("pingList.json read failed")
        with open(str(pingListPath), 'w') as pingList:
            try:
                json.dump(x, pingList)
            except ValueError:
                print("pingList.json write failed")
        

    @tping.command(name="remove", usage=" <role mention>", help="Removes a role from the timed ping list")
    async def remove(self, ctx, role: discord.Role):
        global pingListPath
        guild = ctx.guild.id
        with open(str(pingListPath), 'r') as pingList:
            try:
                x = json.load(pingList)
            except ValueError:
                print("Failed to read to pingList.json")
        with open(str(pingListPath), 'w') as vcWrite:
            try:
                if str(guild) in x:
                    y = x[str(guild)].copy()
                    y[0].pop(str(role.id), None)
                    json.dump(x, vcWrite)
                    #does a check to see if we delete the last entry in json files. Adds {} to json file because json doesn't play nice with empty files.
                    if x == None:
                        x = {}
            except ValueError:
                print("Failed to write to pingList.json")


    @tping.command(name="list", help="Lists all the timed ping roles for the server")
    async def list(self, ctx):
        global pingListPath
        guild = ctx.guild.id
        with open(str(pingListPath), 'r') as pingList:
            try:
                x = json.load(pingList)
                if str(guild) in x:
                    y = x[str(guild)].copy()
                    await ctx.send(y)
            except ValueError:
                print("Failed to read pingList.json")
