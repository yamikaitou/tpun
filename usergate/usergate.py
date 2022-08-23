from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core import data_manager
import discord
import datetime
import time
import json
import logging


class usergate(commands.Cog):
    """
    User gate cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.log = logging.getLogger('red.tpun.usergate')
        self.config = Config.get_conf(
            self,
            identifier=365398642334498816,
            force_registration=True,
        )
        path = data_manager.cog_data_path(cog_instance=self)
        self.userGatePath = path / 'userGate.json'
        if self.userGatePath.exists():
            pass
        else:
            with self.userGatePath.open("w", encoding="utf-8") as f:
                f.write("{}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild.id
        with open(str(self.userGatePath), 'r') as userGate:
            try:
                x = json.load(userGate)
                for guildList, days in x.items():
                    if guildList == str(guild):
                        daysAmount = days
            except ValueError:
                self.log.exception("userGate.json read failed")
        if time.mktime(member.created_at.timetuple()) > (time.mktime(datetime.datetime.now().timetuple()) - (daysAmount * 24 * 60 * 60)):
            await member.kick(reason="Account is under {0} days old".format(str(daysAmount)))

    @commands.guildowner_or_permissions()
    @commands.command(name="usergate")
    async def usergate(self, ctx: commands.Context, days: int):
        """
        Usergate setup command

        Sets the number of days a user's account must exist before joining server, if user does not meet requirement they will get kicked.
        """
        guild = ctx.guild.id
        with open(str(self.userGatePath), 'r') as userGate:
            try:
                x = json.load(userGate)
            except ValueError:
                self.log.exception("userGate.json read failed")
        x.update({str(guild): days})
        with open(str(self.userGatePath), 'w') as userGate:
            try:
                json.dump(x, userGate)
                await ctx.send("Usergate was set to {0} days".format(days))
            except ValueError:
                self.log.exception("userGate.json write failed")
