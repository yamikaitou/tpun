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
            "channeltotmem": 0,
            "channelnewmem": 0,
            "channeltruemem": 0,
            "channeltotbot": 0
        }
        self.config.register_guild(**default_guild)

    async def members(self, guild: discord.Guild):
        true_member_count = len([m for m in ctx.guild.members if not m.bot])
        totmem = guild.member_count
        totmemId: int = await self.config.guild(guild).channeltotmem()
        if totmemId != 0:
            channel: discord.ChannelType = guild.get_channel(totmemId)
            await channel.edit(name='❎ MEMBERS: {} ❎'.format(totmem))
        
        newmemId: int = await self.config.guild(guild).channelnewmem()
        if newmemId != 0:
            channel: discord.ChannelType = guild.get_channel(newmemId)
            prefix: str = ""
            Name: str = "New Members"
            suffix: str = ""
            newmembers: int = 0
            await channel.edit(name='{0} {1} : {2} {3}'.format(prefix, Name, newmembers, suffix))
        await asyncio.sleep(300)

        truememId: int = await self.config.guild(guild).channeltruemem()
        if truememId != 0:
            channel: discord.ChannelType = guild.get_channel(truememId)
            prefix: str = ""
            Name: str = "Users"
            suffix: str = ""
            await channel.edit(name='{0} {1} : {2} {3}'.format(prefix, Name, true_member_count, suffix))
        
        totbotId: int = await self.config.guild(guild).channeltotbot()
        if totbotId != 0:
            channel: discord.ChannelType = guild.get_channel(totbotId)
            prefix: str = ""
            Name: str = "Bots"
            suffix: str = ""
            bot_count: int = totmem - true_member_count
            await channel.edit(name='{0} {1} : {2} {3}'.format(prefix, Name, bot_count, suffix))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.members(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.members(member.guild)

    @commands.group(name="serverhud")
    async def serverhud(self, ctx):
        """
        Base command for all server hud settings
        """
        pass

    @serverhud.command(name="setchannel")
    async def setchannel(self, ctx, type: str, channel: int):
        """
        Sets the channel info type and location

        The command syntax is [p]serverhud setchannel <type> <channel id>
        For a list of channel types use [p]serverhud types
        """
        
        types = ["newmem", "totmem", "totbot", "truemem"]
        for x in types:
            if x == type:
                if x == "newmem":
                    await self.config.guild(ctx.guild).channelnewmem.set(channel)
                    await ctx.send("The new member count channel has been set to <#{}>".format(channel))
                elif x == "totmem":
                    await self.config.guild(ctx.guild).channeltotmem.set(channel)
                    await ctx.send("The total member count channel has been set to <#{}>".format(channel))
                elif x == "totbot":
                    await self.config.guild(ctx.guild).channeltotbot.set(channel)
                    await ctx.send("The total bot count channel has been set to <#{}>".format(channel))
                elif x == "truemem":
                    await self.config.guild(ctx.guild).channeltruemem.set(channel)
                    await ctx.send("The True member count channel has been set to <#{}>".format(channel))
            else:
                pass
        pass

    @serverhud.command(name="types")
    async def types(self, ctx):
        """
        Lists of the different types of channels you can set

        Use [p]serverhud setchannel <type> <channel mention>
        """
        mess = "The avaible types of channels are: new members from today (newmem), total members (totmem), total bots (totbot), True Members (truemem)"
        await ctx.send(mess)
        pass

    @serverhud.command(name="test")
    async def test(self, ctx, event):
        """
        Test the cog to insure functionality

        You can test different events using this command:
        join, leave
        """
        if event == "join" or event == "leave":
            await self.members(ctx.guild)
            await ctx.send("The server channels being tested are: {0}".format(await self.config.guild(ctx.guild).channeltotmem()))
            await ctx.send("Test of the member join/leave event.")
        else:
            await ctx.send("That is not a valid event do [p]help serverhud test for a list of events")