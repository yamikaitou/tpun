from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import datetime
import time



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


     @commands.Cog.listener()
     async def on_member_join(self, member: discord.Member):
          if time.mktime(member.created_at.timetuple()) > (time.mktime(datetime.datetime.now().timetuple()) - 604800):
               await member.kick(reason="Account is under 7 days old")