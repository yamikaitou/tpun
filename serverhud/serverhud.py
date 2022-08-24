from imaplib import Commands
from typing import Literal
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core import data_manager
import discord
import asyncio
import logging
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class serverhud(commands.Cog):
    """
    Cog for creating info channels
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.log = logging.getLogger('red.tpun.serverhud')
        self.config = Config.get_conf(
            self,
            identifier=365398642334498816
        )
        default_guild = {
            "channeltotmem": None,
            "channelnewmem": None,
            "channeltotbot": None
        }
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if self.config.guild(member.guild) is not None:
            channel = await self.config.guild(member.guild).channeltotmem()
            totalMembers = totalMembers + 1
            activeGuilds = self.bot.guilds
            sum = 0
            sum += len(member.guild.members)
            await channel.edit(name='❎ MEMBERS: {} ❎'.format(int(sum)))
        await asyncio.sleep(60)

    @commands.group()
    async def serverhud(self):
        pass

    @serverhud.command(name="setchannel")
    async def setchannel(self, ctx, type: str, channel: discord.channel):
        """
        Sets the channel info type and location

        "For a list of channel types use [p]serverhud types
        """
        
        types = ["newmem", "totmem", "totbot"]
        for x in types:
            if x == type:
                if x == "newmem":
                    await self.config.guild(ctx.guild).newmem.set(channel.id)
                elif x == "totmem":
                    await self.config.guild(ctx.guild).totmem.set(channel.id)
                elif x == "totbot":
                    await self.config.guild(ctx.guild).totbot.set(channel.id)
            else:
                pass
        pass

    @serverhud.command(name="types")
    async def types(self, ctx, type: str, channel: discord.channel):
        """
        Lists of the different types of channels you can set

        Use [p]serverhud setchannel <type> <channel mention>
        """
        mess = "The avaible types of channels are: new members from today (newmem), total members (totmem), total bots (totbot)"
        await ctx.send(mess)
        pass