from typing import Literal
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from datetime import datetime, timedelta
import discord
import asyncio
bot = None
config = None


class listeners(bot, config):
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
            memberList = guild.members
            await self.config.guild(guild).truememcount.set(len([m for m in memberList if not m.bot]))
            await self.config.guild(guild).newmemcount.set(len([m for m in memberList if m.joined_at > datetime.today() - timedelta(days=1)]))
        await self.members(guild)
        await self.boosters(guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if not member.bot:
            memberList = guild.members
            await self.config.guild(guild).truememcount.set(len([m for m in memberList if not m.bot]))
            await self.config.guild(guild).newmemcount.set(len([m for m in memberList if m.joined_at > datetime.today() - timedelta(days=1)]))
        await self.members(guild)
        await self.boosters(guild)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await asyncio.sleep(30)
        if before.guild.premium_subscriber_role not in before.roles and after.guild.premium_subscriber_role in after.roles:
            await self.boosters(before.guild)
        elif before.guild.premium_subscriber_role in before.roles and after.guild.premium_subscriber_role not in after.roles:
            await self.boosters(before.guild)