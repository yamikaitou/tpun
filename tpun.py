from ast import Dict
from typing import Literal
import json
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from mcstatus import MinecraftServer
import discord
import asyncio
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]
import datetime
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

class tpun(commands.Cog):
     """
     TPUN cog
     """

     def __init__(self, bot: Red) -> None:
          self.bot = bot
          self.config = Config.get_conf(
               self,
               identifier=None,
               force_registration=True,
          )

     futureList:Dict = {}
    
     async def checks(self, id, empty, ctx):
          channel = self.bot.get_channel(id)
          await asyncio.sleep(60)
          if len(channel.members) == 0:
               reason = "channel is empty"
               await tpun.delete(self, ctx, reason)
               if empty.done() != True:
                    empty.set_result("Channel deleted because it's empty")
          else:
               await tpun.checks(self, id, empty, ctx)

     def pred(self, emojis, mess1, user: discord.Member):
          return ReactionPredicate.with_emojis(emojis, mess1, user)

     async def emojiSorter(self, ctx, emoji, mess1):
          if emoji == "🎮":
               if ctx.message.author.activity != None:
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

     async def emojiRequest(self, ctx, emoji, mess1, user: discord.Member):
          if emoji == "✅":
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                    try:
                         x = json.load(vcOwners)
                         for vcOwnList, vcNameList in x.items():
                              if vcOwnList == str(user.id):
                                   await self.bot.get_channel(int(vcNameList)).set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True, view_channel=True, use_voice_activation=True, stream=True, connect=True, speak=True, reason="{0} accepted {1}'s request to join their vc: {2}".format(user.name, ctx.author.name, self.bot.get_channel(int(vcNameList)).name))
                                   if ctx.author.voice != None:
                                        if ctx.author.voice.channel.id != vcNameList and ctx.author.voice.channel != None:
                                             await ctx.author.move_to(self.bot.get_channel(int(vcNameList)))
                                   await ctx.send("{0} accepted {1}'s vc request to join: {2}".format(user, ctx.author.name, self.bot.get_channel(int(vcNameList)).mention))
                    except ValueError:
                         await ctx.send("{0} does not own a vc.".format(user.name))
               await mess1.delete()
               

     async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
          # TODO: Replace this with the proper end user data removal handling.
          super().red_delete_data_for_user(requester=requester, user_id=user_id)
     @commands.group(name='minecraft')
     async def minecraft(self, ctx):
          pass
     @minecraft.command(name='help', help="The main help command for t!minecraft")
     async def help(self, ctx):
          await ctx.send("The available commands are status and ip. The available servers are Stoneblock, Luke's Dreamland, Nyx's Server, FTB University. Shorthand for these are stone, luke, nyx, uni")
     @minecraft.command(name='status', usage=" <server>", help="Shows the current status of all server related Minecraft servers, options are: stone, nyx, luke, uni")
     async def status(self, ctx, server):
          invalid = False
          if server == "Stoneblock":
               ip = "142.44.255.131:25574"
          elif server == "Luke's Dreamland":
               ip = "LucidsDreamland.hosting.ethera.net"
          elif server == "Nyx's Server":
               ip =  "209.58.137.109:42568"
          elif server == "FTB University":
               ip =  "tpun.serverminecraft.net"
          elif server == "stone":
               server = "Stoneblock"
               ip =  "142.44.255.131:25574"
          elif server == "luke":
               server = "Luke's Dreamland"
               ip =  "LucidsDreamland.hosting.ethera.net"
          elif server == "nyx":
               ip =  "209.58.137.109:42568"
               server = "Nyx's"
          elif server == "uni":
               server = "FTB University"
               ip =  "localhost"
          else:
               await ctx.send("This server is invalid check available servers using t!minecraft help")
               invalid = True
          if invalid == False:
               mcserver = MinecraftServer.lookup(ip)
               status = mcserver.status()
               await ctx.send("The {0} server has {1} players and replied in {2} ms".format(server, status.players.online, status.latency))
     @minecraft.command(name='ip', usage=" <name>", help="Shows the ip for all server related Minecraft Servers, options are: stone, nyx, luke, uni")
     async def ip(self, ctx, server):
          invalid = False
          if server == "Stoneblock":
               ip = "142.44.255.131:25574"
          elif server == "Luke's Dreamland":
               ip = "LucidsDreamland.hosting.ethera.net"
          elif server == "Nyx's Server":
               ip =  "209.58.137.109:42568"
          elif server == "FTB University":
               ip =  "tpun.serverminecraft.net"
          elif server == "stone":
               server = "Stoneblock"
               ip =  "142.44.255.131:25574"
          elif server == "luke":
               server = "Luke's Dreamland"
               ip =  "LucidsDreamland.hosting.ethera.net"
          elif server == "nyx":
               server = "Nyx's"
               ip =  "209.58.137.109:42568"
          elif server == "uni":
               server = "FTB University"
               ip =  "tpun.serverminecraft.net"
          else:
               await ctx.send("This server is invalid check available servers using t!minecraft help")
               invalid = True
          if invalid == False:
               await ctx.send("The {0} server ip is {1}".format(server, ip))

     @commands.group(name='vc')
     async def vc(self, ctx):
          pass
     @vc.command(name='help', help="Shows all the commands for t!vc")
     async def help(self, ctx, arg):
          if arg == None:
               await ctx.send('That is not a valid command. Use t!vc to see a list of available commands')
          elif arg == 'create':
               await ctx.send("Creates a voice channel with <'name'> t!vc create <'Name'>. You can only have 1 vc. VC deletes after 1 minute of inactivity. You must join your vc within 1 minute or it will be deleted.")
          elif arg == 'delete':
               await ctx.send("Deletes your personal channel, requires a reason t!delete ['reason']. Channels delete on their own after 1 minute of being empty.")
          elif arg == 'gui':
               await ctx.send("Opens the vc creation gui. use t!vc gui")
          elif arg == 'region':
               await ctx.send("Use t!vc region <region> The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa")
          elif arg == 'name':
               await ctx.send("t!vc name Returns the name of your vc")
          elif arg == 'rename':
               await ctx.send("t!vc rename <'name'> Name must be in quotes Renames your personal vc")
          elif arg == 'region':
               await ctx.send("t!vc region <region number> Changes the region of your vc. The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa")
          elif arg == 'lock':
               await ctx.send("t!vc lock Changes your vc to invite only members can join use t!vc invite <@user> to invite someone")
          elif arg == 'unlock':
               await ctx.send("t!vc unlock All verified members can join your vc if unlocked")
          elif arg == 'invite':
               await ctx.send("t!vc invite <@user> Invites a user to your vc")
          elif arg == 'limit':
               await ctx.send("t!vc limit <number> Sets the limit for how many spots are in vc, use 0 to remove limit")
          elif arg == 'request':
               await ctx.send("t!vc request <@user> Sends a user a request to join their vc, request last 5 minutes. You can only request the vc owner to join.")
          elif arg == 'kick':
               await ctx.send("t!vc kick <@user> Kicks a user from your vc")
          elif arg == 'unmute':
               await ctx.send("t!vc unmute <@user> Unmutes a user inside your vc")
          elif arg == 'mute':
               await ctx.send("t!vc mute <@user> Mutes a user inside your vc")
          else:
               await ctx.send("That is not a valid command. Use t!vc to see a list of available commands")

     @vc.command(name='create', usage=" <'name'> name must be in quotes", help="Creates a voice channel with <'name'>. You can only have 1 vc. VC deletes after 1 minute of inactivity. You must join your vc within 1 minute or it will be deleted.")
     async def create(self, ctx, vcName):
          #gets channel for bot message
          dsChannel = 989226756399566919
          channel = self.bot.get_channel(dsChannel)
          #vcrole1 = get(creator.guild.roles, id=703562188224331777)
          if ctx.message.channel.id == dsChannel:
                    category = ctx.channel.category
               jsonPath = "/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json"
               run : bool = True
               if vcName == "":
                    await ctx.send("{0} You need to type a voice channel name t!vc create ['Name']".format(ctx.author.name))
               else:
                    #finds out who called the command, saves author as owner
                    owner = ctx.author.id
                    if vcName == "no activity":
                         await ctx.send("You can't create a game vc if you're not playing a game.")
                         run = False
                    #opens json file for read
                    with open(jsonPath, 'r') as vcOwners:
                    #load vcOwners
                         try:
                              x = json.load(vcOwners)
                              #closes json file from read
                              for vcOwnList, vcId in x.items():
                                   #check if user has a vc by going through vcOwners
                                   if vcOwnList == str(owner):
                                        await ctx.send("{0} You already have a vc created named {1}".format(ctx.author.name, str(self.bot.get_channel(vcId).name)))
                                        run = False
                              if run:
                                   #create vc with arg as name
                                   channel = await ctx.guild.create_voice_channel(vcName, category=category)
                                   await channel.set_permissions(ctx.author, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                                   await channel.set_permissions(ctx.guild.get_role(970379648770928701), view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                                   if ctx.author.voice != None:
                                        if ctx.author.voice.channel.id != channel.id and ctx.author.voice.channel != None:
                                             await ctx.author.move_to(channel)
                                   #create json object nC
                                   vcId = channel.id
                                   nC = {owner : vcId}
                                   x.update(nC)
                                   #add vcOwner and vcId to json
                                   await ctx.send("{0} was created by {1}".format(channel.mention, ctx.author.name))
                                   empty = asyncio.Future()
                                   tpun.futureList[str(vcId)] = empty
                                   asyncio.ensure_future(self.checks(vcId, empty, ctx))

                         except ValueError:
                              if x == "":
                                   x = {}
                    with open(jsonPath, 'w') as vcWrite:
                         try:
                              json.dump(x, vcWrite)
                         except ValueError:
                              print("Minecraft.py Minecraft.create Json write failed.")
    
     @vc.command(name='delete', usage=" ['reason'] reason is optional but if included must be in quotes", help="Deletes your personal channel")
     async def delete(self, ctx, reason = None):
          noVC = "true"
          if reason == None:
               reason = "user deleted their own channel"
          elif reason == "channel is empty":
               noVC = "false"
          run = "false"
          owner = ctx.author.id
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               try:
                    x = json.load(vcOwners)
                    for vcOwnList, idList in x.items():
                         if vcOwnList == str(owner):
                              run = "true"
                              vcId = idList
               except ValueError:
                    await ctx.send("Failed to load vc Owners. Please contact Nado#6969")
          if run == "true":
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'w') as vcWrite:
                    try:
                         channel = self.bot.get_channel(vcId)
                         vcName = str(channel.name)
                         await channel.delete()
                         for id, futa in tpun.futureList.items():
                              if int(id) == vcId:
                                   if futa.done() != True:
                                        futa.set_result("Channel deleted because owner deleted it")
                              else:
                                   pass
                         x.pop(str(owner), None)
                         json.dump(x, vcWrite)
                         #does a check to see if we delete the last entry in json files. Adds {} to json file because json doesn't play nice with empty files.
                         if x == "":
                              x = {}
                         await ctx.send("Succesfully deleted {2}'s voice channel: {0} because {1}".format(vcName, reason, ctx.author.name))
                    except ValueError:
                         await ctx.send("Failed to delete your vc.")
          else:
               if noVC == "true":
                    await ctx.send("{0} You can't delete a VC if you don't have one.".format(ctx.author.name))

     @vc.command(name='name', help="Returns the name of your vc")
     async def name(self, ctx):
          owner = ctx.author.id
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               try:
                    x = json.load(vcOwners)
                    for vcOwnList, vcNameList in x.items():
                         if vcOwnList == str(owner):
                             vcName = self.bot.get_channel(vcNameList).name
                             await ctx.send("{0} Your personal vc is named {1}.".format(ctx.author.name, self.bot.get_channel(vcNameList).mention))
                         else:
                             pass
               except ValueError:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="gui", help="Opens the vc creation gui")
     async def gui(self, ctx):
          #gets channel for bot message
          dsChannel = 989226756399566919
          channel = self.bot.get_channel(dsChannel)
          #vcrole1 = get(creator.guild.roles, id=703562188224331777)
          if ctx.message.channel.id == dsChannel:
               #if any(role.id == 703562188224331777 for role in ctx.message.author.roles):
                    #await creator.remove_roles(vcrole1)
                    #await ctx.send("not important message")
                    #messtag1 = await channel.send('not important') 
                    #await messtag1.delete(delay=None)

                    embed = discord.Embed(color=0xe02522, title='Voice Channel Creator', description= 'Creates a personal voice channel.')
                    embed.set_footer(text='This gui is opened by /vc gui. It allows you to create your own voice channel that will delete itself after 1 minute of being empty. You can delete it by using /vc delete <reason>. 🎮 for game channel, 📱 for social channel, ❓ for other channel')
                    embed.timestamp = datetime.datetime.utcnow()

                    mess1 = await channel.send(embed=embed)
                    emojis = ["🎮","❓", "📱"]
                    start_adding_reactions(mess1, emojis)
                    try:
                         result = await ctx.bot.wait_for("reaction_add", timeout=60.0, check=self.pred(emojis, mess1, ctx.author))
                         emoji = str(result[0])
                         await self.emojiSorter(ctx, emoji, mess1)
                    except asyncio.TimeoutError:
                         await channel.send('Voice channel gui timed out.')
                         await mess1.delete()
                    else:
                         pass

     @vc.command(name="rename", usage=" <'new name'> Name must be in quotes", help="Renames your personal vc")
     async def rename(self, ctx, rename = None):
          if rename == None:
               await ctx.send("{0} Please enter a new name for your vc.".format(ctx.author.name))
          else:
               owner = ctx.author.id
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                    try:
                         x = json.load(vcOwners)
                         for vcOwnList, vcNameList in x.items():
                              if vcOwnList == str(owner):
                                   await self.bot.get_channel(vcNameList).edit(name=rename)
                                   await ctx.send("{0} Your channel's name was changed to {1}".format(ctx.author.name, self.bot.get_channel(vcNameList).mention))
                    except ValueError:
                         await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))
               

     @vc.command(name="region", usage="<region number>", help="Changes the region of your vc. The list of avaliable regions are as follow 0=Auto, 1=US West, 2=US East, 3=US South, 4=EU West, 5=EU Central, 6=Brazil, 7=Hong Kong, 8=Brazil, 9=Japan, 10=Russia, 11=Sydney, 12=South Africa")
     async def region(self, ctx, region):
          if region == "0":
               region = None
               text = "Auto"
          elif region == "1":
               region = "us-west"
               text = "US West"
          elif region == "2":
               region = "us-east"
               text = "US East"
          elif region == "3":
               region = "us-south"
               text = "US South"
          elif region == "4":
               region = "rotterdam"
               text = "Rotterdam"
          elif region == "5":
               region = "singapore"
               text = "Singapore"
          elif region == "6":
               region = "brazil"
               text = "Brazil"
          elif region == "7":
               region = "hongkong"
               text = "Hong Kong"
          elif region == "8":
               region = "india"
               text = "India"
          elif region == "9":
               region = "japan"
               text = "Japan"
          elif region == "10":
               region = "russia"
               text = "Russia"
          elif region == "11":
               region = "sydney"
               text = "Sydney"
          elif region == "12":
               region = "southafrica"
               text = "South Africa"
          elif region == "13":
               region = "south-korea"
               text = "South Korea"
          elif region == "":
               region = None
               text = "Auto"
          else:
               await ctx.send("Something went wrong, please contact Nado#6969")
          
          owner = ctx.author.id
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               try:
                    x = json.load(vcOwners)
                    for vcOwnList, vcNameList in x.items():
                         if vcOwnList == str(owner):
                              await self.bot.get_channel(vcNameList).edit(rtc_region=region)
                              await ctx.send("{0} Your vc: {1} was set to region {2}".format(ctx.author.name, self.bot.get_channel(vcNameList).mention, text))
               except ValueError:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="lock", help="Locks your vc", description="Changes your vc to invite only members can join use t!vc invite <@user> to invite someone")
     async def lock(self, ctx):
          owner = ctx.author.id
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               try:
                    x = json.load(vcOwners)
                    for vcOwnList, vcNameList in x.items():
                         if vcOwnList == str(owner):
                              await self.bot.get_channel(vcNameList).set_permissions(ctx.guild.get_role(970379648770928701), view_channel=True, read_messages=True, send_messages=False, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=False, reason="{0} locked their vc: {1}".format(ctx.author.name, self.bot.get_channel(vcNameList).name))
                              await ctx.send("{0} Your vc: {1} was locked".format(ctx.author.name, self.bot.get_channel(vcNameList).mention))
               except ValueError:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="unlock", help="Unlocks your vc", description="All verified members can join your vc if unlocked")
     async def unlock(self, ctx):
          owner = ctx.author.id
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               try:
                    x = json.load(vcOwners)
                    for vcOwnList, vcNameList in x.items():
                         if vcOwnList == str(owner):
                              await self.bot.get_channel(vcNameList).set_permissions(ctx.guild.get_role(970379648770928701), view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True, reason="{0} unlocked their vc: {1}".format(owner, self.bot.get_channel(vcNameList).name))
                              await ctx.send("{0} Your vc: {1} was unlocked".format(ctx.author.name, self.bot.get_channel(vcNameList).mention))
               except ValueError:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="invite", usage=" <@user>", help="Invites a user to your vc", description="Allow specified user to join your vc")
     async def invite(self, ctx, user: discord.Member=None):
          if user == None:
               await ctx.send("Please mention a user to invite.")
          else:
               owner = ctx.author.id
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                    try:
                         x = json.load(vcOwners)
                         for vcOwnList, vcNameList in x.items():
                              if vcOwnList == str(owner):
                                   await self.bot.get_channel(int(vcNameList)).set_permissions(user, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, stream=True, use_voice_activation=True, speak=True, connect=True, reason="{0} invited {1} to their vc: {2}".format(user.name, ctx.author.name, self.bot.get_channel(int(vcNameList)).name))
                                   await ctx.send("{0} {1} invited you to their vc: {2}".format(user.mention, ctx.author.name, self.bot.get_channel(vcNameList).mention))
                    except ValueError:
                         await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="limit", usage=" <number of users>", help="Sets the limit for how many spots are in vc, use 0 to remove limit")
     async def limit(self, ctx, limit: int = 0):
          owner = ctx.author.id
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               try:
                    x = json.load(vcOwners)
                    for vcOwnList, vcNameList in x.items():
                         if vcOwnList == str(owner):
                              await self.bot.get_channel(vcNameList).edit(user_limit=limit)
                              await ctx.send("{2} The user limit in your vc {0} was changed to {1}".format(self.bot.get_channel(vcNameList).mention, limit, ctx.author.name))
               except ValueError:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="request", usage="<@user>", help="Sends a user a request to join their vc, request last 5 minutes")
     async def request(self, ctx, user: discord.Member=None):
          #gets channel for bot message
          if user == None:
               await ctx.send("{0} Please mention a user to request to join".format(ctx.author.name))
          else:
               if user.id == ctx.author.id:
                    await ctx.send("{0} you silly goose! You can't request to join your own vc.".format(ctx.author.name))
               else:
                    dsChannel = 989226756399566919
                    channel = self.bot.get_channel(dsChannel)
                    if ctx.message.channel.id == dsChannel:

                         embed = discord.Embed(color=0xe02522, title='Voice Channel Request', description= '{0}: {1} is requesting to join your channel'.format(user.mention, ctx.author.name))
                         embed.set_footer(text='React with ✅ below to accept this request')
                         embed.timestamp = datetime.datetime.utcnow()

                         mess1 = await channel.send(embed=embed)
                         emojis = ["✅"]
                         start_adding_reactions(mess1, emojis)
                         try:
                              result = await ctx.bot.wait_for("reaction_add", timeout=300.0, check=self.pred(emojis, mess1, user))
                              emoji = str(result[0])
                              await self.emojiRequest(ctx, emoji, mess1, user)
                         except asyncio.TimeoutError:
                              await channel.send('This request timed out.')
                              await mess1.delete()
                         except 404:
                              await channel.send("This request timed out")
                              await mess1.delete()
                    else:
                         pass

     @vc.command(name="kick", usage="<@user>", help="Kicks a user from your vc")
     async def kick(self, ctx, user: discord.Member=None):
          if user == None:
               await ctx.send("{0} Please mention a user to kick.".format(ctx.author.name))
          else:
               owner = ctx.author.id
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                    try:
                         x = json.load(vcOwners)
                         for vcOwnList, vcNameList in x.items():
                              if vcOwnList == str(owner):
                                   await self.bot.get_channel(int(vcNameList)).set_permissions(user, view_channel=True, read_messages=True, send_messages=False, read_message_history=True, stream=False, use_voice_activation=True, speak=False, connect=False, reason="{0} kicked {1} from their vc: {2}".format(ctx.author.name, user.name, self.bot.get_channel(vcNameList).name))
                                   if user.voice != None:
                                        if user.voice.channel.id == vcNameList:
                                             await user.move_to(None)
                                   await ctx.send("{0} was kicked from your vc: {1}".format(user.name, self.bot.get_channel(vcNameList).mention))
                    except ValueError:
                         await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="mute", usage="<@user>", help="Mutes a user inside your vc")
     async def mute(self, ctx, user: discord.Member = None):
          if user == None:
               await ctx.send("{0} Please mention a user to mute.".format(ctx.author.name))
          else:
               owner = ctx.author.id
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                    try:
                         x = json.load(vcOwners)
                         for vcOwnList, vcNameList in x.items():
                              if vcOwnList == str(owner):
                                   await self.bot.get_channel(vcNameList).set_permissions(user, view_channel=True, read_messages=True, send_messages=False, read_message_history=True, use_voice_activation=True, stream=True, connect=True, speak=False, reason="{0} muted {1} in their vc: {2}".format(ctx.author.name, user.name, self.bot.get_channel(vcNameList).name))
                                   if user.voice.channel.id == vcNameList:
                                        await user.move_to(self.bot.get_channel(vcNameList))
                                   await ctx.send("{0} was muted in your vc: {1}".format(user.name, self.bot.get_channel(vcNameList).mention))
                    except ValueError:
                         await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="unmute", usage="<@user>", help="Unmutes a user inside your vc")
     async def unmute(self, ctx, user: discord.Member = None):
          if user == None:
               await ctx.send("{0} Please mention a user to unmute.".format(ctx.author.name))
          else:
               owner = ctx.author.id
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                    try:
                         x = json.load(vcOwners)
                         for vcOwnList, vcNameList in x.items():
                              if vcOwnList == str(owner):
                                   await self.bot.get_channel(vcNameList).set_permissions(user, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, stream=True, use_voice_activation=True, connect=True, speak=True, reason="{0} unmuted {1} in their vc: {2}".format(ctx.author.name, user.name, self.bot.get_channel(vcNameList).name))
                                   if user.voice.channel.id == vcNameList:
                                        await user.move_to(self.bot.get_channel(vcNameList))
                                   await ctx.send("{0} was unmuted in your vc: {1}".format(user.name, self.bot.get_channel(vcNameList).mention))
                    except ValueError:
                         await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))