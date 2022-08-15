from multiprocessing.sharedctypes import Value
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import datetime
import time
import json
from redbot.core import data_manager



class usergate(commands.Cog):
     """
     User gate cog
     """

     def __init__(self, bot: Red) -> None:
          self.bot = bot
          self.config = Config.get_conf(
               self,
               identifier=None,
               force_registration=True,
          )
          global userGatePath
          path = data_manager.cog_data_path(cog_instance=self)
          userGatePath = path / 'userGate.json'
          if userGatePath.exists():
               pass
          else:
               with userGatePath.open("w", encoding ="utf-8") as f:
                    f.write("{}")

     @commands.Cog.listener()
     async def on_member_join(self, member: discord.Member):
          global userGatePath
          guild = member.guild.id
          with open(str(userGatePath), 'r') as userGate:
               try:
                    x = json.load(userGate)
                    for guildList, days in x.items():
                         if guildList == str(guild):
                              daysAmount = days
               except ValueError:
                    print("userGate.json read failed")
          if time.mktime(member.created_at.timetuple()) > (time.mktime(datetime.datetime.now().timetuple()) - (days * 24 * 60 * 60)):
               await member.kick(reason="Account is under {0} days old".format(str(days)))

     @commands.guildowner_or_permissions()
     @commands.command(name="usergate", usage="<days>", help="Sets the number of days a user's account must exist before joining server, if user does not meet requirement they will get kicked.")
     async def usergate(self, ctx, days : int):
          global userGatePath
          guild = ctx.guild.id
          with open(str(userGatePath), 'r') as userGate:
               try:
                    x = json.load(userGate)
               except ValueError:
                    print("userGate.json read failed")
          x.update({str(guild) : days})
          print(x)
          with open(str(userGatePath), 'w') as userGate:
               try:
                    json.dump(x, userGate)
               except ValueError:
                    print("userGate.json write failed")