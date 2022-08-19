from ast import Dict
from types import GeneratorType
from typing import Generator, Literal
from io import TextIOWrapper
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import json
import discord
import asyncio
import datetime
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class pvc(commands.Cog):
    """
    Private voice channel cog
    """

    def getpaths(self):

        global vcOwnersPath
        path = data_manager.cog_data_path(cog_instance=self)
        vcOwnersPath = path / 'vcOwners.json'
        if not vcOwnersPath.exists():
            with vcOwnersPath.open("w", encoding="utf-8") as f:
                f.write("{}")

        global vcRolesPath
        vcRolesPath = path / 'vcRoles.json'
        if not vcRolesPath.exists():
            with vcRolesPath.open("w", encoding="utf-8") as f:
                f.write("{}")

        global vcChannelsPath
        vcChannelsPath = path / 'vcChannels.json'
        if not vcChannelsPath.exists():
            with vcChannelsPath.open("w", encoding="utf-8") as f:
                f.write("{}")

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )
        self.getpaths()



    futureList: Dict = {}

    def vcOwnerRead(self, guild, owner):
        global vcOwnersPath
        try:
            with open(str(vcOwnersPath), 'r') as vcOwners:
                x = json.load(vcOwners)
                for server, vcs in x.items():
                    if server == str(guild):
                        for i in vcs:
                            for vcOwner, vcId in i.items():
                                if vcOwner == str(owner):
                                    voiceChannel = self.bot.get_channel(int(vcId))
                                    return voiceChannel
        except ValueError:
            print("read failed")
            return None

    def getVcList(self, guild):
        global vcOwnersPath
        try:
            with open(str(vcOwnersPath), 'r') as vcOwners:
                x = json.load(vcOwners)
                for server, vcs in x.items():
                    if server == str(guild):
                        for i in vcs:
                            print(i)
                            return i
        except ValueError:
            print("read failed")
            return None

    def vcChannelRead(self, ctx: commands.Context):
        global vcChannelsPath
        try:
            with open(str(vcChannelsPath), 'r') as vcChannels:
                x = json.load(vcChannels)
                for server, channel in x.items():
                    if server == str(ctx.guild.id):
                        return self.bot.get_channel(int(channel))

        except ValueError:
            print("read failed")
            return None

    def vcRoleRead(self, ctx: commands.Context):
        global vcRolesPath
        rolesObj = []
        try:
            with open(str(vcRolesPath), 'r') as vcRoles:
                x = json.load(vcRoles)
                for server, roles in x.items():
                    if server == str(ctx.guild.id) and type(roles) == list:
                        return roles
        except ValueError:
            print("read failed")
            return None

    async def checks(self, id, empty, ctx: commands.Context):
        channel = self.bot.get_channel(id)
        while empty.done() is not True:
            await asyncio.sleep(60)
            if len(channel.members) == 0:
                reason = "channel is empty"
                await pvc.delete(self, ctx, reason)
                pvc.futureList.pop(str(id), None)
                break
            else:
                pass

    def pred(self, emojis, mess1, user: discord.Member):
        return ReactionPredicate.with_emojis(emojis, mess1, user)

    async def emojisorter(self, ctx: commands.Context, emoji, mess1):
        if emoji == "🎮":
            if ctx.message.author.activity is not None:
                for activity in ctx.message.author.activities:
                    if activity.type == discord.activity.ActivityType.playing:
                        await self.create(ctx, str(activity.name))
                    else:
                        await self.create(ctx, "no activity")
            else:
                await self.create(ctx, "no activity")
            await mess1.delete()
        elif emoji == "📱":
            await self.create(ctx, ctx.author.name + "'s social channel")
            await mess1.delete()
        elif emoji == "❓":
            await self.create(ctx, ctx.author.name + "'s private vc")
            await self.lock(ctx)
            await mess1.delete()

    async def emojiRequest(self, ctx: commands.Context, emoji, mess1, user: discord.Member):
        if emoji == "✅":
            voiceChannel = await self.vcOwnerRead(self, ctx.guild.id, user.id)
            if voiceChannel is not None:
                await voiceChannel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True, view_channel=True, use_voice_activation=True, stream=True, connect=True, speak=True, reason="{0} accepted {1}'s request to join their vc: {2}".format(user.name, ctx.author.name, voiceChannel.name))
                if ctx.author.voice is not None:
                    if ctx.author.voice.channel.id != voiceChannel.id and ctx.author.voice.channel is not None:
                        await ctx.author.move_to(voiceChannel)
                        await ctx.send("{0} accepted {1}'s vc request to join: {2}".format(user, ctx.author.name, voiceChannel.mention))
            else:
                await ctx.send("{0} does not own a vc.".format(user.name))
            await mess1.delete()

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.group(name='vc')
    async def vc(self, ctx: commands.Context):
        pass

    @vc.command(name='create', usage=" <'name'> name must be in quotes", help="Creates a voice channel with <'name'>. You can only have 1 vc. VC deletes after 1 minute of inactivity. You must join your vc within 1 minute or it will be deleted.")
    async def create(self, ctx: commands.Context, *, vcName):
        global vcOwnersPath
        dsChannel = self.vcChannelRead(ctx)
        roleList = self.vcRoleRead(ctx)
        guild = ctx.guild.id
        x = None
        if ctx.message.channel.id == dsChannel.id:
            category = ctx.channel.category
            run: bool = True
            if vcName == "":
                await ctx.send("{0} You need to type a voice channel name t!vc create ['Name']".format(ctx.author.name))
            else:
                owner = ctx.author.id
                if vcName == "no activity":
                    await ctx.send("You can't create a game vc if you're not playing a game.")
                    run = False
            try:
                with open(str(vcOwnersPath), 'r') as vcOwners:
                    x = json.load(vcOwners)
                    vc = self.vcOwnerRead(guild, ctx.author.id)
                    if vc:
                        await ctx.send("{0} You already have a vc created named {1}".format(ctx.author.name, str(vc.name)))
                        run = False
                    if run:
                        channel = await ctx.guild.create_voice_channel(vcName, category=category)
                        await channel.set_permissions(ctx.author, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                        for role in roleList:
                            await channel.set_permissions(ctx.guild.get_role(role), view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                        if ctx.author.voice is not None and ctx.author.voice.channel.id != channel.id and ctx.author.voice.channel is not None:
                            await ctx.author.move_to(channel)
                        vcId = channel.id
                        nC = {owner: vcId}
                        if str(guild) in x:
                            y = x[str(guild)].copy()
                            y[0].update(nC)
                        else:
                            x.update({str(guild): [{}]})
                            y = x[str(guild)].copy()
                            y[0].update(nC)
                        await ctx.send("{0} was created by {1}".format(channel.mention, ctx.author.name))
                        empty = asyncio.Future()
                        pvc.futureList[str(vcId)] = empty
                        asyncio.ensure_future(self.checks(vcId, empty, ctx))
            except ValueError:
                pass
            with open(str(vcOwnersPath), 'w') as vcWrite:
                try:
                    json.dump(x, vcWrite)
                except ValueError:
                    print("pvc.create Json write failed.")
        else:
            await ctx.send("This command only works in the custom vc {0} channel.".format(dsChannel.mention))

    @vc.command(name='delete', usage=" ['reason'] reason is optional but if included must be in quotes", help="Deletes your personal channel")
    async def delete(self, ctx: commands.Context, reason=None):
        global vcOwnersPath
        noVC = True
        if reason is None:
            reason = "user deleted their own channel"
        elif reason == "channel is empty":
            noVC = False
        run = False
        owner = ctx.author.id
        with open(str(vcOwnersPath), 'r') as vcOwners:
            try:
                x = json.load(vcOwners)
                vc = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
                if vc:
                    run = True
                    vcId = vc.id
                    for id, futa in pvc.futureList.items():
                        if int(id) == vcId and futa.done() is not True:
                            futa.set_result(reason)
                            pvc.futureList.pop(str(vcId), None)
                            break
            except ValueError:
                await ctx.send("Failed to load vc Owners.")
        if run:
            with open(str(vcOwnersPath), 'w') as vcWrite:
                try:
                    channel = self.bot.get_channel(vcId)
                    vcName = str(channel.name)
                    await channel.delete()
                    if str(ctx.guild.id) in x:
                        y = x[str(ctx.guild.id)].copy()
                        y[0].pop(str(owner), None)
                    json.dump(x, vcWrite)
                    if x is None:
                        x = "{}"
                    await ctx.send("Succesfully deleted {2}'s voice channel: {0} because {1}".format(vcName, reason, ctx.author.name))
                except ValueError:
                    await ctx.send("Failed to delete your vc.")
        else:
            if noVC:
                await ctx.send("{0} You can't delete a VC if you don't have one.".format(ctx.author.name))

    @vc.command(name='name', help="Returns the name of your vc")
    async def name(self, ctx: commands.Context):
        voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
        if voiceChannel is not None:
            await ctx.send("{0} Your personal vc is named {1}.".format(ctx.author.name, voiceChannel.mention))
        else:
            await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name='list', help="Lists all the owners of vc's")
    async def list(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        embed = discord.Embed(title="VC Owners", description="All of the owners of private voice channels in the server are listed below", color=0xc72327)
        i = self.getVcList(guild)
        for vcOwner, vcId in i[0].items():
            voiceChannel: discord.VoiceChannel = self.bot.get_channel(int(vcId))
            name: discord.Member = await guild.fetch_member(vcOwner)
            message = "<#" + str(voiceChannel.id) + ">" + " ⌇ " + name.mention
            embed.add_field(name="🔊", value=message, inline=True)
        await ctx.send(embed=embed)

    @vc.command(name="gui", help="Opens the vc creation gui")
    async def gui(self, ctx: commands.Context):
        dsChannel = self.vcChannelRead(ctx)
        if ctx.message.channel.id == dsChannel.id:
            embed = discord.Embed(color=0xe02522, title='Voice Channel Creator', description='Creates a personal voice channel.')
            embed.set_footer(text='This gui is opened by /vc gui. It allows you to create your own voice channel that will delete itself after 1 minute of being empty. You can delete it by using /vc delete <reason>. 🎮 for game channel, 📱 for social channel, ❓ for other channel')
            embed.timestamp = datetime.datetime.utcnow()
            mess1 = await ctx.channel.send(embed=embed)
            emojis = ["🎮", "❓", "📱"]
            start_adding_reactions(mess1, emojis)
            try:
                result = await ctx.bot.wait_for("reaction_add", timeout=180.0, check=self.pred(emojis, mess1, ctx.author))
                emoji = str(result[0])
                await self.emojisorter(ctx, emoji, mess1)
            except asyncio.TimeoutError:
                await ctx.channel.send('Voice channel gui timed out.')
                await mess1.delete()
            else:
                pass

    @vc.command(name="rename", usage=" <'new name'> Name must be in quotes", help="Renames your personal vc")
    async def rename(self, ctx: commands.Context, *, rename=None):
        if rename is None:
            await ctx.send("{0} Please enter a new name for your vc.".format(ctx.author.name))
        else:
            voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
            if voiceChannel is not None:
                await voiceChannel.edit(name=rename)
                await ctx.send("{0} Your channel's name was changed to {1}".format(ctx.author.name, voiceChannel.mention))
            else:
                await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    def getRegion(self, int):
        conditions = {
            1: "us-west",
            2: "us-east",
            3: "us-south",
            4: "rotterdam",
            5: "singapore",
            6: "brazil",
            7: "hongkong",
            8: "india",
            9: "japan",
            10: "russia",
            11: "sydney",
            12: "southafrica",
            13: "south-korea"
        }
        if int in conditions.keys():
            return conditions[int]

    @vc.command(name="region", usage="<region number>", help="Changes the region of your vc. The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa")
    async def region(self, ctx: commands.Context, region: int):
        region1 = self.getRegion(region)
        message = region1
        voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
        if voiceChannel is not None:
            if region1 is None:
                region1 = None
                message = "auto"
            await voiceChannel.edit(rtc_region=region1)
            await ctx.send("{0} Your vc: {1} was set to region {2}".format(ctx.author.name, voiceChannel.mention, message))
        else:
            await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="lock", help="Locks your vc", description="Changes your vc to invite only members can join use t!vc invite <@user> to invite someone")
    async def lock(self, ctx: commands.Context):
        roleList = self.vcRoleRead(ctx)
        voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
        if voiceChannel is not None:
            for role in roleList:
                await voiceChannel.set_permissions(ctx.guild.get_role(role), view_channel=True, read_messages=True, send_messages=False, read_message_history=True, use_voice_activation=True, speak=True, connect=False, reason="{0} locked their vc: {1}".format(ctx.author.name, voiceChannel.name))
            await ctx.send("{0} Your vc: {1} was locked".format(ctx.author.name, voiceChannel.mention))
        else:
            await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="unlock", help="Unlocks your vc", description="All verified members can join your vc if unlocked")
    async def unlock(self, ctx: commands.Context):
        owner = ctx.author.id
        roleList = self.vcRoleRead(ctx)
        voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
        if voiceChannel is not None:
            for role in roleList:
                await voiceChannel.set_permissions(ctx.guild.get_role(role), view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, speak=True, connect=True, reason="{0} unlocked their vc: {1}".format(owner, voiceChannel.name))
            await ctx.send("{0} Your vc: {1} was unlocked".format(ctx.author.name, voiceChannel.mention))
        else:
            await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="invite", usage=" <@user>", help="Invites a user to your vc", description="Allow specified user to join your vc")
    async def invite(self, ctx: commands.Context, user: discord.Member):
        if user is None:
            await ctx.send("Please mention a user to invite.")
        else:
            voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
            if voiceChannel is not None:
                await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, speak=True, connect=True, reason="{0} invited {1} to their vc: {2}".format(user.name, ctx.author.name, voiceChannel.name))
                await ctx.send("{0} {1} invited you to their vc: {2}".format(user.mention, ctx.author.name, voiceChannel.mention))
            else:
                await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="limit", usage=" <number of users>", help="Sets the limit for how many spots are in vc, use 0 to remove limit")
    async def limit(self, ctx: commands.Context, limit: int = 0):
        voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
        if voiceChannel is not None:
            await voiceChannel.edit(user_limit=limit)
            await ctx.send("{2} The user limit in your vc {0} was changed to {1}".format(voiceChannel.mention, limit, ctx.author.name))
        else:
            await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="request", usage="<@user>", help="Sends a user a request to join their vc, request last 5 minutes")
    async def request(self, ctx: commands.Context, user: discord.Member):
        if user is None:
            await ctx.send("{0} Please mention a user to request to join".format(ctx.author.name))
        else:
            if user.id == ctx.author.id:
                await ctx.send("{0} you silly goose! You can't request to join your own vc.".format(ctx.author.name))
            else:
                dsChannel = self.vcChannelRead(ctx)
                if ctx.message.channel.id == dsChannel.id:
                    embed = discord.Embed(color=0xe02522, title='Voice Channel Request', description='{0}: {1} is requesting to join your channel'.format(user.mention, ctx.author.name))
                    embed.set_footer(text='React with ✅ below to accept this request')
                    embed.timestamp = datetime.datetime.utcnow()
                    mess1 = await ctx.channel.send(embed=embed)
                    emojis = ["✅"]
                    start_adding_reactions(mess1, emojis)
                    try:
                        result = await ctx.bot.wait_for("reaction_add", timeout=300.0, check=self.pred(emojis, mess1, user))
                        emoji = str(result[0])
                        await self.emojiRequest(ctx, emoji, mess1, user)
                    except asyncio.TimeoutError:
                        await ctx.channel.send('This request timed out.')
                        await mess1.delete()
                    except 404:
                        await ctx.channel.send("This request timed out")
                        await mess1.delete()
                    else:
                        pass

    @vc.command(name="kick", usage="<@user>", help="Kicks a user from your vc")
    async def kick(self, ctx: commands.Context, user: discord.Member):
        if user is None:
            await ctx.send("{0} Please mention a user to kick.".format(ctx.author.name))
        else:
            voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
            if voiceChannel is not None:
                await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=False, read_message_history=True, stream=False, use_voice_activation=True, speak=False, connect=False, reason="{0} kicked {1} from their vc: {2}".format(ctx.author.name, user.name, voiceChannel.name))
                if user.voice is not None:
                    if user.voice.channel.id == voiceChannel.id:
                        await user.move_to(None)
                        await ctx.send("{0} was kicked from your vc: {1}".format(user.name, voiceChannel.mention))
                else:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="mute", usage="<@user>", help="Mutes a user inside your vc")
    async def mute(self, ctx: commands.Context, user: discord.Member):
        if user is None:
            await ctx.send("{0} Please mention a user to mute.".format(ctx.author.name))
        else:
            voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
            if voiceChannel is not None:
                await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=False, read_message_history=True, use_voice_activation=True, stream=False, connect=True, speak=False, reason="{0} muted {1} in their vc: {2}".format(ctx.author.name, user.name, voiceChannel.name))
                if user.voice.channel.id == voiceChannel.idt:
                    await user.move_to(voiceChannel)
                await ctx.send("{0} was muted in your vc: {1}".format(user.name, voiceChannel.mention))
            else:
                await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="unmute", usage="<@user>", help="Unmutes a user inside your vc")
    async def unmute(self, ctx: commands.Context, user: discord.Member):
        if user is None:
            await ctx.send("{0} Please mention a user to unmute.".format(ctx.author.name))
        else:
            voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
            if voiceChannel is not None:
                await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, stream=True, use_voice_activation=True, connect=True, speak=True, reason="{0} unmuted {1} in their vc: {2}".format(ctx.author.name, user.name, voiceChannel.name))
                if user.voice.channel.id == voiceChannel.id:
                    await user.move_to(voiceChannel)
                await ctx.send("{0} was unmuted in your vc: {1}".format(user.name, voiceChannel.mention))
            else:
                await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

    @vc.command(name="claim", usage="", help="Claims a voice channel from another user if they're not in it.")
    async def claim(self, ctx: commands.Context):
        global vcOwnersPath
        owner: int = 0
        newOwner = str(ctx.author.id)
        channelid = ctx.author.voice.channel.id
        newWrite = {newOwner: channelid}
        x = None
        vcEmpty = False
        guild = ctx.guild.id
        if channelid is not None:
            with open(str(vcOwnersPath), 'r') as vcOwners:
                try:
                    x = json.load(vcOwners)
                    for server, vcs in x.items():
                        if server == str(guild):
                            for i in vcs:
                                for vcOwnList, vcNameList in i.items():
                                    if int(vcNameList) == int(channelid):
                                        owner = int(vcOwnList)
                                        ownerObj = await self.bot.get_or_fetch_member(ctx.guild, owner)
                                        if ownerObj.voice is None or ownerObj.voice.channel.id != channelid:
                                            await ctx.send("{0} has claimed {1}".format(ctx.author.mention, self.bot.get_channel(vcNameList).mention))
                                            await self.bot.get_channel(vcNameList).set_permissions(ctx.author, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                                            y = x[str(guild)].copy()
                                            y[0].pop(str(owner), None)
                                            y[0].update(newWrite)
                                            break
                                        else:
                                            await ctx.send("<@{0}> is still in their vc you can only run this when they have left".format(owner))
                except ValueError:
                    await ctx.send("{0} is not a valid channel id for a personal vc.".format(channelid))
            with open(str(vcOwnersPath), 'w') as vcWrite:
                try:
                    json.dump(x, vcWrite)
                except ValueError:
                    print("vcOwners.json write failed.")

    @vc.command(name="transfer", usage=" <@user>", help="Transfers a voice channel to another user")
    async def transfer(self, ctx: commands.Context, newOwner: discord.Member):
        global vcOwnersPath
        owner = str(ctx.author.id)
        if ctx.author.voice is not None:
            channelid = ctx.author.voice.channel.id
            newWrite = {str(newOwner.id): int(channelid)}
            x = None
            vcEmpty = False
            guild = ctx.guild
            if channelid is not None:
                with open(str(vcOwnersPath), 'r') as vcOwners:
                    try:
                        x = json.load(vcOwners)
                        vcObj = self.vcOwnerRead(guild.id, ctx.author.id)
                        ownerObj = await self.bot.get_or_fetch_member(guild, ctx.author.id)
                        y = x[str(guild.id)].copy()
                        if vcObj is not None and vcObj.id == channelid:
                            if ownerObj.voice.channel.id == channelid and str(newOwner.id) not in y[0].keys() and str(guild.id) in x:
                                await ctx.send("{0} has transfered vc ownership to {1}".format(ctx.author.mention, vcObj.mention))
                                y[0].pop(str(owner), None)
                                y[0].update(newWrite)
                            elif str(newOwner.id) in y[0].keys():
                                await ctx.send("{0} already owns a vc".format(newOwner.display_name))
                            else:
                                await ctx.send("<@{0}> you must be in your vc to run this command".format(ctx.author.id))
                        else:
                            await ctx.send("You don't own this voice channel.")
                    except ValueError:
                        await ctx.send("{0} is not a valid channel id for a personal vc.".format(channelid))
                with open(str(vcOwnersPath), 'w') as reputationWrite:
                    try:
                        json.dump(x, reputationWrite)
                    except ValueError:
                        print("vcOwners.json write failed.")
        else:
            await ctx.send("You can only run this command while you are in your voice channel.")

    @commands.guildowner_or_permissions()
    @vc.command(name="setup", help="Set's up a channel for creating custom vc's in, please put this channel in the category you would like all custom vc's to be made in")
    async def setup(self, ctx: commands.Context):
        global vcRolesPath
        global vcChannelsPath
        global vcOwnersPath
        guild = ctx.guild.id
        run: bool = True
        x: TextIOWrapper
        y: TextIOWrapper
        with open(str(vcOwnersPath), 'r') as vcChannels:
            try:
                x = json.load(vcChannels)
                for server, channel in x.items():
                    if server == str(guild):
                        run = False
            except ValueError:
                run = False
                print("vcchannel.json failed to read")
        if run:
            channel = await ctx.guild.create_text_channel("personal-vc-commands")
            mess0 = await ctx.send("Make sure to put the personal-vc-commands channel in the category you wish channels to be made in. You may rename the channel to whatever you wish.")
            newWrite = {str(guild): channel.id}
            x.update(newWrite)
            with open(str(vcChannelsPath), 'w') as vcChannelsWrite:
                try:
                    json.dump(x, vcChannelsWrite)
                except ValueError:
                    print("vcchannels.json write failed.")
        mess1 = await ctx.send("Please ping any roles you wish to have permissions to join channels on creation. These roles will also be used for unlock/lock commands. If you wish to allow anyone to join on creation type 'none'.")

        def check(m):
            return m.channel == mess1.channel

        msg = await self.bot.wait_for('message', check=check, timeout=600)
        roles = []
        if msg.content != "none":
            for i in msg.role_mentions:
                roles.append(i.id)
        else:
            roles.append(ctx.guild.id)
        await mess1.delete()
        with open(str(vcRolesPath), 'r') as vcRoles:
            try:
                y = json.load(vcRoles)
                y.update({str(guild): roles})
            except ValueError:
                print("vcroles.json read failed.")
        with open(str(vcRolesPath), 'w') as vcRolesWrite:
            try:
                json.dump(y, vcRolesWrite)
            except ValueError:
                print("vcroles.json write failed.")
        with open(str(vcOwnersPath), 'r') as vcOwnersRead:
            try:
                x = json.load(vcOwnersRead)
            except ValueError:
                print("vcOwners.json read failed")
        with open(str(vcOwnersPath), 'w') as vcOwnersWrite:
            try:
                x.update({str(guild): [{}]})
                json.dump(x, vcOwnersWrite)
            except ValueError:
                print("vcOwners.json write failed")
        mess2 = await ctx.send("Your settings are currently: {0} as the channel and {1} are the public roles that will be used.".format(channel.name, roles))
        await asyncio.sleep(30)
        await mess0.delete()
        await mess2.delete()

    @commands.admin()
    @vc.command(name="clear_settings", help="Clears the personal vc commands channel allowing for fresh setup")
    async def clear_settings(self, ctx: commands.Context):
        global vcChannelsPath
        global vcRolesPath
        run: bool = False
        run2: bool = False
        with open(str(vcChannelsPath), 'r') as vcChannels:
            try:
                x = json.load(vcChannels)
                for server, channel in x.items():
                    if server == str(ctx.guild.id):
                        run = True
            except ValueError:
                print("vcchannel.json failed to read")
        if run:
            x.pop(str(ctx.guild.id), None)
            with open(str(vcChannelsPath), 'w') as vcChannelsWrite:
                try:
                    json.dump(x, vcChannelsWrite)
                except ValueError:
                    print("vcchannels.json write failed.")
        else:
            await ctx.send("Your server is not setup yet")
        with open(str(vcRolesPath), 'r') as vcRoles:
            try:
                y = json.load(vcRoles)
                for server, channel in y.items():
                    if server == str(ctx.guild.id):
                        run2 = True
            except ValueError:
                print("vcroles.json read failed.")
        if run2:
            y.pop(str(ctx.guild.id), None)
            with open(str(vcRolesPath), 'w') as vcRolesWrite:
                try:
                    json.dump(y, vcRolesWrite)
                except ValueError:
                    print("vcroles.json write failed.")
        if run and run2:
            await ctx.send("Your server's vc data has been cleared.")
