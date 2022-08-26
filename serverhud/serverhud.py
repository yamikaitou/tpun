from imaplib import Commands
from typing import Literal
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core import data_manager
import discord
import asyncio
import logging
from datetime import date, datetime, timedelta
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
            "booster": {
                "channel": 0,
                "prefix": "",
                "name": "Boosters",
                "suffix": ""
            },
            "boosterbar": {
                "channel": 0,
                "prefix": "",
                "stylefull": "*",
                "styleempty": "-"
            },
            "truememcount": 0,
            "newmemcount": 0,
            "newmemget": datetime.today()
        }
        self.config.register_guild(**default_guild)

    async def members(self, guild: discord.Guild):
        true_member_count = await self.config.guild(guild).truememcount()
        newmembers = await self.config.guild(guild).newmemcount()
        totmem = guild.member_count
        totmemDict = await self.config.guild(guild).totmem()
        totmemId = totmemDict["channel"]
        if totmemId != 0:
            channel: discord.ChannelType = guild.get_channel(totmemId)
            await channel.edit(name='{0} {1}: {2} {3}'.format(totmemDict["prefix"], totmemDict["name"], totmem, totmemDict["suffix"]))
            await asyncio.sleep(15)
            pass

        newmemObj = await self.config.guild(guild).newmem()
        newmemId = newmemObj["channel"]
        if newmemId != 0:
            channel: discord.ChannelType = guild.get_channel(newmemId)
            await channel.edit(name='{0} {1}: {2} {3}'.format(newmemObj["prefix"], newmemObj["name"], newmembers, newmemObj["suffix"]))
            await asyncio.sleep(15)
            pass

        truememObj = await self.config.guild(guild).truemem()
        truememId = truememObj["channel"]
        if truememId != 0:
            channel: discord.ChannelType = guild.get_channel(truememId)
            await channel.edit(name='{0} {1}: {2} {3}'.format(truememObj["prefix"], truememObj["name"], true_member_count, truememObj["suffix"]))
            await asyncio.sleep(15)
            pass

        totbotObj = await self.config.guild(guild).totbot()
        totbotId = totbotObj["channel"]
        if totbotId != 0:
            channel: discord.ChannelType = guild.get_channel(totbotId)
            bot_count: int = totmem - true_member_count
            await channel.edit(name='{0} {1}: {2} {3}'.format(totbotObj["prefix"], totbotObj["name"], bot_count, totbotObj["suffix"]))
            await asyncio.sleep(15)
            pass

    async def boosters(self, guild: discord.Guild):
        booster_count: int = guild.premium_subscription_count
        boosterObj = await self.config.guild(guild).booster()
        boosterId = boosterObj["channel"]
        if boosterId != 0:
            channel: discord.ChannelType = guild.get_channel(boosterId)
            await channel.edit(name='{0} {1}: {2} {3}'.format(boosterObj["prefix"], boosterObj["name"], booster_count, boosterObj["suffix"]))
            await asyncio.sleep(15)
            pass

        boosterBarObj = await self.config.guild(guild).boosterbar()
        boosterBarId = boosterBarObj["channel"]
        mess = ""
        stylefull = boosterBarObj["stylefull"]
        styleempty = boosterBarObj["styleempty"]
        if boosterBarId != 0:
            channel: discord.ChannelType = guild.get_channel(boosterBarId)
            if booster_count < 2:
                for i in range(booster_count):
                    mess = mess + stylefull
                for i in range(2 - booster_count):
                    mess = mess + styleempty
                await channel.edit(name='{0}Lvl 1{1}'.format(boosterBarObj["prefix"], mess))
                await asyncio.sleep(15)
            elif booster_count < 7:
                for i in range(booster_count):
                    mess = mess + stylefull
                for i in range(7 - booster_count):
                    mess = mess + styleempty
                await channel.edit(name='{0}Lvl 2{1}'.format(boosterBarObj["prefix"], mess))
                await asyncio.sleep(15)
            elif booster_count < 14:
                for i in range(booster_count - 7):
                    mess = mess + stylefull
                for i in range(14 - booster_count):
                    mess = mess + styleempty
                await channel.edit(name='{0}Lvl 3{1}'.format(boosterBarObj["prefix"], mess))
                await asyncio.sleep(15)
            elif booster_count > 14:
                for i in range(7):
                    mess = mess + stylefull
                await channel.edit(name='{0}Max{1}'.format(boosterBarObj["prefix"], mess))
                await asyncio.sleep(15)     

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if not member.bot:
            truememcount = await self.config.guild(member.guild).truememcount()
            newcount = truememcount + 1
            await self.config.guild(member.guild).truememcount.set(newcount)
            newmemcount = await self.config.guild(guild).newmemcount()
            changeNewMem = newmemcount + 1
            await self.config.guild(guild).newmemcount.set(changeNewMem)
        if self.newMemGet < (datetime.today() - timedelta(days=1)):
            truemem = await self.config.guild(guild).truemem()
            memberList = guild.members
            await self.config.guild(guild).truememcount.set(len([m for m in memberList if not m.bot]))
            await self.config.guild(guild).newmemcount.set(len([m for m in memberList if m.joined_at > datetime.today() - timedelta(days=1)]))
            self.newMemGet = datetime.today()
        await self.members(guild)
        await self.boosters(guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if not member.bot:
            truememcount = await self.config.guild(guild).truememcount()
            newcount = truememcount - 1
            await self.config.guild(guild).truememcount.set(newcount)
            newmemcount = await self.config.guild(guild).newmemcount()
            changeNewMem = newmemcount - 1
            await self.config.guild(guild).newmemcount.set(changeNewMem)
        if self.newMemGet < (datetime.today() - timedelta(days=1)):
            truemem = self.config.guild(guild).truemem()
            memberList = guild.members
            await self.config.guild(guild).truememcount.set(len([m for m in memberList if not m.bot]))
            await self.config.guild(guild).newmemcount.set(len([m for m in memberList if m.joined_at > datetime.today() - timedelta(days=1)]))
            self.newMemGet = datetime.today()
        await self.members(guild)
        await self.boosters(guild)

    @commands.group(name="serverhud")
    async def serverhud(self, ctx):
        """
        Base command for all server hud settings
        """
        pass

    @commands.guildowner_or_permissions()
    @serverhud.command(name="setchannel")
    async def setchannel(self, ctx, type: str, channel: int):
        """
        Sets the channel info type and location

        The command syntax is [p]serverhud setchannel <type> <channel id>
        For a list of channel types use [p]serverhud types
        """
        
        types = ["newmem", "totmem", "totbot", "truemem", "booster", "boosterbar"]
        for x in types:
            if x == type:
                if x == "newmem":
                    newmemDict: dict = await self.config.guild(ctx.guild).newmem()
                    newmemDict.update({"channel": channel})
                    await self.config.guild(ctx.guild).newmem.set(newmemDict)
                    await ctx.send("The new member count channel has been set to <#{}>".format(channel))
                elif x == "totmem":
                    totmemDict: dict = await self.config.guild(ctx.guild).totmem()
                    totmemDict.update({"channel": channel})
                    await self.config.guild(ctx.guild).totmem.set(totmemDict)
                    await ctx.send("The total member count channel has been set to <#{}>".format(channel))
                elif x == "totbot":
                    totbotDict: dict = await self.config.guild(ctx.guild).totbot()
                    totbotDict.update({"channel": channel})
                    await self.config.guild(ctx.guild).totbot.set(totbotDict)
                    await ctx.send("The total bot count channel has been set to <#{}>".format(channel))
                elif x == "truemem":
                    truememDict: dict = await self.config.guild(ctx.guild).truemem()
                    truememDict.update({"channel": channel})
                    await self.config.guild(ctx.guild).truemem.set(truememDict)
                    await ctx.send("The True member count channel has been set to <#{}>".format(channel))
                elif x == "booster":
                    boosterDict: dict = await self.config.guild(ctx.guild).booster()
                    boosterDict.update({"channel": channel})
                    await self.config.guild(ctx.guild).booster.set(boosterDict)
                    await ctx.send("The Booster count channel has been set to <#{}>".format(channel))
                elif x == "boosterbar":
                    boosterBarDict: dict = await self.config.guild(ctx.guild).boosterbar()
                    boosterBarDict.update({"channel": channel})
                    await self.config.guild(ctx.guild).boosterbar.set(boosterBarDict)
                    await ctx.send("The Booster count channel has been set to <#{}>".format(channel))
            else:
                pass
        pass

    @commands.guildowner_or_permissions()
    @serverhud.command(name="setprefix")
    async def setprefix(self, ctx, type: str, *, prefix: str):
        """
        Sets the prefix for this type of info channel

        For a list of channel types use [p]serverhud types
        """
        types = ["newmem", "totmem", "totbot", "truemem", "booster", "boosterbar"]
        for x in types:
            if x == type:
                if x == "newmem":
                    newmemDict: dict = await self.config.guild(ctx.guild).newmem()
                    newmemDict.update({"prefix": prefix})
                    await self.config.guild(ctx.guild).newmem.set(newmemDict)
                    await ctx.send("The new member count prefix has been set to {}".format(prefix))
                elif x == "totmem":
                    totmemDict: dict = await self.config.guild(ctx.guild).totmem()
                    totmemDict.update({"prefix": prefix})
                    await self.config.guild(ctx.guild).totmem.set(totmemDict)
                    await ctx.send("The total member count prefix has been set to {}".format(prefix))
                elif x == "totbot":
                    totbotDict: dict = await self.config.guild(ctx.guild).totbot()
                    totbotDict.update({"prefix": prefix})
                    await self.config.guild(ctx.guild).totbot.set(totbotDict)
                    await ctx.send("The total bot count prefix has been set to {}".format(prefix))
                elif x == "truemem":
                    truememDict: dict = await self.config.guild(ctx.guild).truemem()
                    truememDict.update({"prefix": prefix})
                    await self.config.guild(ctx.guild).truemem.set(truememDict)
                    await ctx.send("The True member count prefix has been set to {}".format(prefix))
                elif x == "booster":
                    boosterDict: dict = await self.config.guild(ctx.guild).booster()
                    boosterDict.update({"prefix": prefix})
                    await self.config.guild(ctx.guild).booster.set(boosterDict)
                    await ctx.send("The Booster count prefix has been set to {}".format(prefix))
                elif x == "boosterbar":
                    boosterBarDict: dict = await self.config.guild(ctx.guild).boosterbar()
                    boosterBarDict.update({"prefix": prefix})
                    await self.config.guild(ctx.guild).boosterbar.set(boosterBarDict)
                    await ctx.send("The Booster Bar prefix has been set to {}".format(prefix))
            else:
                pass
        pass

    @commands.guildowner_or_permissions()
    @serverhud.command(name="setsuffix")
    async def setsuffix(self, ctx, type: str, *, suffix: str):
        """
        Sets the suffix for this type of info channel

        For a list of channel types use [p]serverhud types
        """
        types = ["newmem", "totmem", "totbot", "truemem", "booster"]
        for x in types:
            if x == type:
                if x == "newmem":
                    newmemDict: dict = await self.config.guild(ctx.guild).newmem()
                    newmemDict.update({"suffix": suffix})
                    await self.config.guild(ctx.guild).newmem.set(newmemDict)
                    await ctx.send("The new member count suffix has been set to {}".format(suffix))
                elif x == "totmem":
                    totmemDict: dict = await self.config.guild(ctx.guild).totmem()
                    totmemDict.update({"suffix": suffix})
                    await self.config.guild(ctx.guild).totmem.set(totmemDict)
                    await ctx.send("The total member count suffix has been set to {}".format(suffix))
                elif x == "totbot":
                    totbotDict: dict = await self.config.guild(ctx.guild).totbot()
                    totbotDict.update({"suffix": suffix})
                    await self.config.guild(ctx.guild).totbot.set(totbotDict)
                    await ctx.send("The total bot count suffix has been set to {}".format(suffix))
                elif x == "truemem":
                    truememDict: dict = await self.config.guild(ctx.guild).truemem()
                    truememDict.update({"suffix": suffix})
                    await self.config.guild(ctx.guild).truemem.set(truememDict)
                    await ctx.send("The True member count suffix has been set to {}".format(suffix))
                elif x == "booster":
                    boosterDict: dict = await self.config.guild(ctx.guild).booster()
                    boosterDict.update({"suffix": suffix})
                    await self.config.guild(ctx.guild).booster.set(boosterDict)
                    await ctx.send("The Booster count prefix has been set to {}".format(suffix))
            else:
                pass
        pass

    @commands.guildowner_or_permissions()
    @serverhud.command(name="setname")
    async def setname(self, ctx, type: str, *, name: str):
        """
        Sets the name for this type of info channel

        For a list of channel types use [p]serverhud types
        """
        types = ["newmem", "totmem", "totbot", "truemem", "booster"]
        for x in types:
            if x == type:
                if x == "newmem":
                    newmemDict: dict = await self.config.guild(ctx.guild).newmem()
                    newmemDict.update({"name": name})
                    await self.config.guild(ctx.guild).newmem.set(newmemDict)
                    await ctx.send("The new member count name has been set to {}".format(name))
                elif x == "totmem":
                    totmemDict: dict = await self.config.guild(ctx.guild).totmem()
                    totmemDict.update({"name": name})
                    await self.config.guild(ctx.guild).totmem.set(totmemDict)
                    await ctx.send("The total member count name has been set to {}".format(name))
                elif x == "totbot":
                    totbotDict: dict = await self.config.guild(ctx.guild).totbot()
                    totbotDict.update({"name": name})
                    await self.config.guild(ctx.guild).totbot.set(totbotDict)
                    await ctx.send("The total bot count name has been set to {}".format(name))
                elif x == "truemem":
                    truememDict: dict = await self.config.guild(ctx.guild).truemem()
                    truememDict.update({"name": name})
                    await self.config.guild(ctx.guild).truemem.set(truememDict)
                    await ctx.send("The True member count name has been set to {}".format(name))
                elif x == "booster":
                    boosterDict: dict = await self.config.guild(ctx.guild).booster()
                    boosterDict.update({"name": name})
                    await self.config.guild(ctx.guild).booster.set(boosterDict)
                    await ctx.send("The Booster count prefix has been set to {}".format(name))
            else:
                pass
        pass

    @commands.guildowner_or_permissions()
    @serverhud.command(name="setstyle")
    async def setstyle(self, ctx, type, *, style: str):
        """
        Set's the style of the booster bar

        Valid types are full and empty
        """
        if type == "full":
            boosterBarDict: dict = await self.config.guild(ctx.guild).boosterbar()
            boosterBarDict.update({"stylefull": style})
            await self.config.guild(ctx.guild).boosterbar.set(boosterBarDict)
            await ctx.send("The Booster Bar full style has been set to {}".format(style))
        elif type == "empty":
            boosterBarDict: dict = await self.config.guild(ctx.guild).boosterbar()
            boosterBarDict.update({"styleempty": style})
            await self.config.guild(ctx.guild).boosterbar.set(boosterBarDict)
            await ctx.send("The Booster Bar empty style has been set to {}".format(style))
        else:
            await ctx.send("That is not a valid booster bar type")
        

    @commands.guildowner_or_permissions()
    @serverhud.command(name="types")
    async def types(self, ctx):
        """
        Lists of the different types of channels you can set

        Use [p]serverhud setchannel <type> <channel mention>
        """
        mess = "The avaible types of channels are: new members from today (newmem), total members (totmem), total bots (totbot), True Members (truemem), Server Boosters Count (booster), Booster Bar (boosterbar)"
        await ctx.send(mess)
        pass

    @commands.guildowner_or_permissions()
    @serverhud.command(name="test")
    async def test(self, ctx, event):
        """
        Test the cog to insure functionality

        You can test different events using this command:
        join, leave
        """
        if event == "join" or event == "leave":
            memberList = ctx.guild.members
            await self.config.guild(ctx.guild).truememcount.set(len([m for m in memberList if not m.bot]))
            await self.config.guild(ctx.guild).newmemcount.set(len([m for m in memberList if m.joined_at > datetime.today() - timedelta(days=1)]))
            self.newMemGet = datetime.today()
            await self.members(ctx.guild)
            await self.boosters(ctx.guild)
            await ctx.send("Test of the member join/leave event.")
        else:
            await ctx.send("That is not a valid event do [p]help serverhud test for a list of events")