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
            "totmem": {
                "channel": 0,
                "prefix": "",
                "name": "Total Members",
                "suffix": ""
            },
            "newmem": {
                "channel": 0,
                "prefix": "",
                "name": "New Members",
                "suffix": ""
            },
            "truemem": {
                "channel": 0,
                "prefix": "",
                "name": "Total Users",
                "suffix": ""
            },
            "totbot": {
                "channel": 0,
                "prefix": "",
                "name": "Total Bots",
                "suffix": ""
            },
        }
        self.config.register_guild(**default_guild)

    async def members(self, guild: discord.Guild):
        true_member_count = len([m for m in guild.members if not m.bot])
        totmem = guild.member_count
        totmemId: int = await self.config.guild(guild).totmem.channel()
        if totmemId != 0:
            channel: discord.ChannelType = guild.get_channel(totmemId)
            prefix: str = await self.config.guild(guild).totmem.prefix()
            Name: str = await self.config.guild(guild).totmem.name()
            suffix: str = await self.config.guild(guild).totmem.suffix()
            await channel.edit(name='{0} {1}: {2} {3}'.format(prefix, Name, totmem, suffix))
        
        newmemId: int = await self.config.guild(guild).newmem.channel()
        if newmemId != 0:
            channel: discord.ChannelType = guild.get_channel(newmemId)
            prefix: str = await self.config.guild(guild).newmem.prefix()
            Name: str = await self.config.guild(guild).newmem.name()
            suffix: str = await self.config.guild(guild).newmem.suffix()
            newmembers: int = 0
            await channel.edit(name='{0} {1}: {2} {3}'.format(prefix, Name, newmembers, suffix))

        truememId: int = await self.config.guild(guild).truemem.channel()
        if truememId != 0:
            channel: discord.ChannelType = guild.get_channel(truememId)
            prefix: str = await self.config.guild(guild).truemem.prefix()
            Name: str = await self.config.guild(guild).truemem.name()
            suffix: str = await self.config.guild(guild).truemem.suffix()
            prefix: str = ""
            Name: str = "Users"
            suffix: str = ""
            await channel.edit(name='{0} {1}: {2} {3}'.format(prefix, Name, true_member_count, suffix))
        
        totbotId: int = await self.config.guild(guild).totbot.channel()
        if totbotId != 0:
            channel: discord.ChannelType = guild.get_channel(totbotId)
            prefix: str = await self.config.guild(guild).totbot.prefix()
            Name: str = await self.config.guild(guild).totbot.name()
            suffix: str = await self.config.guild(guild).totbot.suffix()
            prefix: str = ""
            Name: str = "Bots"
            suffix: str = ""
            bot_count: int = totmem - true_member_count
            await channel.edit(name='{0} {1}: {2} {3}'.format(prefix, Name, bot_count, suffix))

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
                    await self.config.guild(ctx.guild).newmem.channel.set(channel)
                    await ctx.send("The new member count channel has been set to <#{}>".format(channel))
                elif x == "totmem":
                    await self.config.guild(ctx.guild).totmem.channel.set(channel)
                    await ctx.send("The total member count channel has been set to <#{}>".format(channel))
                elif x == "totbot":
                    await self.config.guild(ctx.guild).totbot.channel.set(channel)
                    await ctx.send("The total bot count channel has been set to <#{}>".format(channel))
                elif x == "truemem":
                    await self.config.guild(ctx.guild).truemem.channel.set(channel)
                    await ctx.send("The True member count channel has been set to <#{}>".format(channel))
            else:
                pass
        pass

    @serverhud.command(name="setprefix")
    async def setprefix(self, ctx, type: str, *, prefix: str):
        """
        Sets the prefix for this type of info channel

        For a list of channel types use [p]serverhud types
        """
        types = ["newmem", "totmem", "totbot", "truemem"]
        for x in types:
            if x == type:
                if x == "newmem":
                    await self.config.guild(ctx.guild).newmem.prefix.set(prefix)
                    await ctx.send("The new member count prefix has been set to <#{}>".format(prefix))
                elif x == "totmem":
                    await self.config.guild(ctx.guild).totmem.prefix.set(prefix)
                    await ctx.send("The total member count prefix has been set to <#{}>".format(prefix))
                elif x == "totbot":
                    await self.config.guild(ctx.guild).totbot.prefix.set(prefix)
                    await ctx.send("The total bot count prefix has been set to <#{}>".format(prefix))
                elif x == "truemem":
                    await self.config.guild(ctx.guild).truemem.prefix.set(prefix)
                    await ctx.send("The True member count prefix has been set to <#{}>".format(prefix))
            else:
                pass
        pass

    @serverhud.command(name="setsuffix")
    async def setsuffix(self, ctx, type: str, *, suffix: str):
        """
        Sets the suffix for this type of info channel

        For a list of channel types use [p]serverhud types
        """
        types = ["newmem", "totmem", "totbot", "truemem"]
        for x in types:
            if x == type:
                if x == "newmem":
                    await self.config.guild(ctx.guild).newmem.suffix.set(suffix)
                    await ctx.send("The new member count suffix has been set to <#{}>".format(suffix))
                elif x == "totmem":
                    await self.config.guild(ctx.guild).totmem.suffix.set(suffix)
                    await ctx.send("The total member count suffix has been set to <#{}>".format(suffix))
                elif x == "totbot":
                    await self.config.guild(ctx.guild).totbot.suffix.set(suffix)
                    await ctx.send("The total bot count suffix has been set to <#{}>".format(suffix))
                elif x == "truemem":
                    await self.config.guild(ctx.guild).truemem.suffix.set(suffix)
                    await ctx.send("The True member count suffix has been set to <#{}>".format(suffix))
            else:
                pass
        pass

    @serverhud.command(name="setname")
    async def setname(self, ctx, type: str, *, name: str):
        """
        Sets the name for this type of info channel

        For a list of channel types use [p]serverhud types
        """
        types = ["newmem", "totmem", "totbot", "truemem"]
        for x in types:
            if x == type:
                if x == "newmem":
                    await self.config.guild(ctx.guild).newmem.name.set(name)
                    await ctx.send("The new member count name has been set to <#{}>".format(name))
                elif x == "totmem":
                    await self.config.guild(ctx.guild).totmem.name.set(name)
                    await ctx.send("The total member count name has been set to <#{}>".format(suffix))
                elif x == "totbot":
                    await self.config.guild(ctx.guild).totbot.name.set(name)
                    await ctx.send("The total bot count name has been set to <#{}>".format(name))
                elif x == "truemem":
                    await self.config.guild(ctx.guild).truemem.name.set(name)
                    await ctx.send("The True member count name has been set to <#{}>".format(name))
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