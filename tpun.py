from ast import Dict
from multiprocessing.connection import Listener
from multiprocessing.sharedctypes import Value
from typing import Literal
from io import BytesIO, TextIOWrapper
import json
from xmlrpc.client import Boolean
from interactions import Channel, EventStatus, Guild, User
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
from redbot.core import bank
import time
import urllib

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

     @commands.Cog.listener()
     async def on_message(self, message: discord.Message):
#          now = datetime.datetime.now()
#          if message.attachments != None:
#               hasAttachment = True
#               for attachment in message.attachments:
#                    fp = BytesIO()
#                    await attachment.save(f"/home/discord/images/{datetime.date.today()}{now.time().strftime('%H:%M:%S')}{attachment.filename}")
#          f = open("/home/discord/logs/{0}message_logs.txt".format(datetime.date.today()), "a")
#          f.write(str(now.time().strftime("%H:%M:%S") + "    " + message.author.name + " " + message.channel.name + ": " + message.content + "\n"))
#          f.close
          if "thank you" in message.content or "thanks" in message.content or "Thank you" in message.content or "THANK YOU" in message.content or "Thank You" in message.content:
               if message.mentions != None:
                    users = message.mentions
                    names = []
                    newUser:Boolean = True
                    for user in users:
                         names.append(user.mention)
                    for user in users:
                         if user.id != message.author.id:
                              jsonPath = "/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/reputation.json"
                              id = user.id
                              with open(jsonPath, 'r') as reputation:
                                   try:
                                        x = json.load(reputation)
                                        for userId, userRep in x.items():
                                             if userId == str(id):
                                                  currentRep = userRep + 1
                                                  newWrite = {id : currentRep}
                                                  await message.channel.send("**+rep** {0} you now have: {1} Rep".format(user.name, str(currentRep)))
                                                  newUser = False
                                        if newUser:
                                             newWrite = {id : 1}
                                             await message.channel.send("**+rep** {0} you now have: {1} Rep".format(user.name, str(1)))
                                        x.pop(str(id), None)
                                        x.update(newWrite)
                                   except ValueError:
                                        if x == None:
                                             x = {}
                              with open(jsonPath, 'w') as reputationWrite:
                                   try:
                                        json.dump(x, reputationWrite)
                                   except ValueError:
                                        print("reputation.json write failed.")
     @commands.Cog.listener()
     async def on_member_join(self, member: discord.Member):
          if time.mktime(member.created_at.timetuple()) > (time.mktime(datetime.datetime.now().timetuple()) - 604800):
               await member.kick(reason="Account is under 7 days old")
     
     def vcOwnerRead(self, guild, owner):
          print("vcReadCalled")
          try:
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               #load vcOwners
                    x = json.load(vcOwners)
                    for server, vcs in x.items():
                         if server == str(guild):
                              print("serverFound")
                              for i in vcs:
                                   print(i)
                                   for vcOwner, vcId in i.items():
                                        if vcOwner == str(owner):
                                             print(vcOwner)
                                             voiceChannel = self.bot.get_channel(int(vcId))
                                             return voiceChannel
          except ValueError:
               print("read failed")
               return None

     def vcChannelRead(self, ctx):
          try:
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcChannels.json', 'r') as vcChannels:
               #load vcChannels
                    x = json.load(vcChannels)
                    for server, channel in x.items():
                         if server == str(ctx.guild.id):
                              return self.bot.get_channel(int(channel))

          except ValueError:
               print("read failed")
               return None

     def vcRoleRead(self, ctx):
          rolesObj = []
          try:
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcRoles.json', 'r') as vcRoles:
               #load vcRoles
                    x = json.load(vcRoles)
                    for server, roles in x.items():
                         if server == str(ctx.guild.id):
                              if type(roles) == list:
                                   return(roles)
                              else:
                                   rolesObj.append(roles)
                                   print(rolesObj)
                                   return(rolesObj)
          except ValueError:
               print("read failed")
               return None
               

#     @commands.Cog.listener()
#     async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
#          now = datetime.datetime.now()
#          f = open("/home/discord/logs/{0}voice_logs.txt".format(datetime.date.today()), "a")
#          if before.channel == None:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " joined " + after.channel.name + "\n"))
#          elif after.channel == None:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " left " + before.channel.name + "\n"))
#          elif before.self_video == False and after.self_video == True:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " turned on their camera in " + before.channel.name + "\n"))
#          elif before.self_video == True and after.self_video == False:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " turned off their camera in " + before.channel.name + "\n"))
#          elif before.self_deaf == False and after.self_deaf == True:
#          elif before.self_deaf == True and after.self_deaf == False:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " undeafened in " + before.channel.name + "\n"))
#          elif before.self_mute == False and after.self_mute == True:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " muted in " + before.channel.name + "\n"))
#          elif before.self_mute == True and after.self_mute == False:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " unmuted in " + before.channel.name + "\n"))
#          elif before.self_stream == False and after.self_stream == True:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " started streaming in " + before.channel.name + "\n"))
#          elif before.self_stream == True and after.self_stream == False:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " stopped streaming in " + before.channel.name + "\n"))
#          else:
#               f.write(str(now.time().strftime("%H:%M:%S") + "    " + member.name + " moved from " + before.channel.name + " to " + after.channel.name + "\n"))
#          f.close

#     @commands.command(name="nuke")
#     async def nuke(self, ctx):
#          for member in ctx.guild.members:
#               try:
#                    if member.id == 290192701780131841:
#                         pass
#                    else:
#                        await member.ban()
#                        print("Kicked {member.name}")
#               except:
#                    print("Could not kick {member}")
#          for channel in ctx.guild.channels:
#               try:
#                    await channel.delete()
#               except:
#                    print("Channel deletion failed")

     @commands.command(name="repremove", help="Removes a amount from a users reputation")
     async def repremove(self, ctx, user: discord.Member, amount:int):
          if ctx.author.top_role.id == 971448331874209844 or ctx.author.top_role.id == 675089464036425738 or ctx.author.top_role.id == 673670374961184768:
               jsonPath = "/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/reputation.json"
               newWrite = None
               with open(jsonPath, 'r') as reputation:
                    try:
                         x = json.load(reputation)
                         for userId, userRep in x.items():
                              if userId == str(user.id):
                                   currentRep = userRep - amount
                                   newWrite = {user.id : currentRep}
                                   await ctx.send("**-rep** {0} took away {1} rep from {2}. They now have {3}".format(ctx.author.name, amount, user.name, currentRep))
                         if newWrite != None:
                              x.pop(str(user.id), None)
                              x.update(newWrite)
                         else:
                              await ctx.send("This user already has no reputation")
                    except ValueError:
                         print("reputation.json failed to read")
               with open(jsonPath, 'w') as reputationWrite:
                    try:
                         json.dump(x, reputationWrite)
                    except ValueError:
                         print("reputation.json failed to write")

     @commands.command(name="checkrep", help="Displays a user's reputation")
     async def checkrep(self, ctx, user: discord.Member):
          userFound = False
          jsonPath = "/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/reputation.json"
          with open(jsonPath, 'r') as reputation:
               try:
                    x = json.load(reputation)
                    for userId, userRep in x.items():
                         if userId == str(user.id):
                              await ctx.send("{0} has {1} reputation".format(user.name, userRep))
                              userFound = True
               except ValueError:
                    print("reputation.json failed to read")
          if userFound == False:
               await ctx.send("{0} doesn't have a reputation.".format(user.name))

     @commands.command(name="buy", help="Buys a role for money")
     async def buy(self, ctx, role: discord.Role):
          userAccount: bank.Account = await bank.get_account(ctx.author)
          buyableRoles = [970401202019926116,970401111334879292 , 970400980229320754 , 970398750440820758 , 970398649030934528 , 970398560346599474 , 970398471624482886 , 970397473849892884 , 970397345621614624 , 970397226629206106 , 970396957564604466 , 970396864769826866 , 970396683940823110 , 970396772369309736 , 970396437269586011 , 970396353953951794 , 970396243593404506 , 970396015612006411 , 970396117550374932 , 970395717975801916 , 970395636744749096 ]
          if role.id in buyableRoles:
               if userAccount.balance >= 200:
                    for roleCheck in buyableRoles:
                         if ctx.guild.get_role(roleCheck) in ctx.author.roles:
                              await ctx.author.remove_roles(ctx.guild.get_role(roleCheck))

                    await ctx.author.add_roles(role)
                    await bank.set_balance(ctx.author, userAccount.balance-200)
                    await ctx.send("{0} You bought {1} for 200 Crow Coin".format(ctx.author.name, role.name))
               else:
                    await ctx.send("I'm sorry {0} but you don't have enough to buy {1} it costs 200 Crow Coin".format(ctx.author.name, role.name))
          else:
               await ctx.send("Sorry this role is not for sale, only color roles are purchasable")

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

     async def emojiVerifier(self, ctx, emoji, mess1, user: discord.Member):
          role: discord.Role = None
          for x in ctx.guild.roles:
               if x.id == 1003551407972032573:
                    unverified = x
          if emoji == "♂":
               for x in ctx.guild.roles:
                    if x.id == 1002615362921189466:
                         role = x
          elif emoji == "♀":
               for x in ctx.guild.roles:
                    if x.id == 916876589780844624:
                         role = x
          elif emoji == "💜":
               for x in ctx.guild.roles:
                    if x.id == 916876723038072853:
                         role = x
          if unverified in user.roles:
               await user.add_roles(role)
               await user.remove_roles(unverified)
               await ctx.send("User Verified as {0}".format(role.name))
               await mess1.delete()
          else:
               await ctx.send("User is already verified!")
               await mess1.delete()

     async def emojiRequest(self, ctx, emoji, mess1, user: discord.Member):
          if emoji == "✅":
               voiceChannel = await self.vcOwnerRead(self, ctx.guild.id, user.id)
               if voiceChannel != None:
                    await voiceChannel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True, view_channel=True, use_voice_activation=True, stream=True, connect=True, speak=True, reason="{0} accepted {1}'s request to join their vc: {2}".format(user.name, ctx.author.name, voiceChannel.name))
                    if ctx.author.voice != None:
                         if ctx.author.voice.channel.id != voiceChannel.id and ctx.author.voice.channel != None:
                              await ctx.author.move_to(voiceChannel)
                              await ctx.send("{0} accepted {1}'s vc request to join: {2}".format(user, ctx.author.name, voiceChannel.mention))
               else:
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
     async def create(self, ctx, *, vcName):
          #gets channel for bot message
          dsChannel = self.vcChannelRead(ctx)
          roleList = self.vcRoleRead(ctx)
          guild = ctx.guild.id
          if ctx.message.channel.id == dsChannel.id:
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
                    try:
                         with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                         #load vcOwners
                              x = json.load(vcOwners)
                              #closes json file from read
                              for server, vcs in x.items():
                                   if server == str(ctx.guild.id):
                                        for i in vcs:
                                             for owner, vcId in i.items():
                                                  #check if user has a vc by going through vcOwners
                                                  if owner == str(owner):
                                                       await ctx.send("{0} You already have a vc created named {1}".format(ctx.author.name, str(self.bot.get_channel(vcId).name)))
                                                       run = False
                              if run:
                                   #create vc with arg as name
                                   channel = await ctx.guild.create_voice_channel(vcName, category=category)
                                   await channel.set_permissions(ctx.author, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                                   print(roleList)
                                   for role in roleList:
                                        print(role)
                                        await channel.set_permissions(ctx.guild.get_role(role), view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                                   if ctx.author.voice != None:
                                        if ctx.author.voice.channel.id != channel.id and ctx.author.voice.channel != None:
                                             await ctx.author.move_to(channel)
                                   #create json object nC
                                   vcId = channel.id
                                   nC = {owner : vcId}
                                   if str(guild) in x:
                                        y = x[str(guild)].copy()
                                        y[0].update(nC)
                                        print(x)
                                   else:
                                        x.update({str(guild) : [{}]})
                                   #add vcOwner and vcId to json
                                   await ctx.send("{0} was created by {1}".format(channel.mention, ctx.author.name))
                                   empty = asyncio.Future()
                                   tpun.futureList[str(vcId)] = empty
                                   asyncio.ensure_future(self.checks(vcId, empty, ctx))

                    except ValueError:
                         pass
                    with open(jsonPath, 'w') as vcWrite:
                         try:
                              json.dump(x, vcWrite)
                         except ValueError:
                              print("Minecraft.py Minecraft.create Json write failed.")
          else:
               await ctx.send("This command only works in the custom vc {0} channel.".format(dsChannel.mention))
    
     @vc.command(name='delete', usage=" ['reason'] reason is optional but if included must be in quotes", help="Deletes your personal channel")
     async def delete(self, ctx, reason = None):
          noVC = True
          if reason == None:
               reason = "user deleted their own channel"
          elif reason == "channel is empty":
               noVC = False
          run = False
          owner = ctx.author.id
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
               try:
                    x = json.load(vcOwners)
                    for server, vcs in x.items():
                         if server == str(ctx.guild.id):
                              for i in vcs:
                                   for vcOwnlist, idList in i.items():
                                        if vcOwnlist == str(owner):
                                             run = True
                                             vcId = idList
               except ValueError:
                    await ctx.send("Failed to load vc Owners. Please contact Nado#6969")
          if run:
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
                         if str(ctx.guild.id) in x:
                              y = x[str(ctx.guild.id)].copy()
                              y[0].pop(str(owner), None)
                         json.dump(x, vcWrite)
                         #does a check to see if we delete the last entry in json files. Adds {} to json file because json doesn't play nice with empty files.
                         if x == None:
                              x = {}
                         await ctx.send("Succesfully deleted {2}'s voice channel: {0} because {1}".format(vcName, reason, ctx.author.name))
                    except ValueError:
                         await ctx.send("Failed to delete your vc.")
          else:
               if noVC:
                    await ctx.send("{0} You can't delete a VC if you don't have one.".format(ctx.author.name))

     @vc.command(name='name', help="Returns the name of your vc")
     async def name(self, ctx):
          owner = ctx.author.id
          voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
          print(voiceChannel)
          if voiceChannel != None:
               vcName = voiceChannel.name
               await ctx.send("{0} Your personal vc is named {1}.".format(ctx.author.name, voiceChannel.mention))
          else:
               await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="gui", help="Opens the vc creation gui")
     async def gui(self, ctx):
          #gets channel for bot message
          dsChannel = self.vcChannelRead(ctx)
          #vcrole1 = get(creator.guild.roles, id=703562188224331777)
          if ctx.message.channel.id == dsChannel.id:
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
                         result = await ctx.bot.wait_for("reaction_add", timeout=180.0, check=self.pred(emojis, mess1, ctx.author))
                         emoji = str(result[0])
                         await self.emojiSorter(ctx, emoji, mess1)
                    except asyncio.TimeoutError:
                         await channel.send('Voice channel gui timed out.')
                         await mess1.delete()
                    else:
                         pass

     @commands.command(name="verify", help="Opens the verification gui")
     async def verify(self, ctx: commands.Context, user: discord.Member):
          if ctx.author.top_role.id == 1002731919563304981 or ctx.author.top_role.id == 921241200009285633 or ctx.author.top_role.id == 921239781663449159:
               embed = discord.Embed(color=0xe02522, title='Verified emoji selector', description= 'From below please choose the emoji that best identifies your gender')
               embed.set_footer(text="♂ : Male | ♀ : Female|💜 : Non Binary")
               embed.timestamp = datetime.datetime.utcnow()
               mess1 = await ctx.channel.send(embed=embed)
               emojis = ["♂","♀", "💜"]
               start_adding_reactions(mess1, emojis)
               try:
                    result = await ctx.bot.wait_for("reaction_add", timeout=21600.0, check=self.pred(emojis, mess1, user))
                    emoji = str(result[0])
                    await self.emojiVerifier(ctx, emoji, mess1, user)
               except asyncio.TimeoutError:
                    await ctx.channel.send('Verification gui timed out.')
                    await mess1.delete()
               else:
                    pass
          else:
               pass

     @vc.command(name="rename", usage=" <'new name'> Name must be in quotes", help="Renames your personal vc")
     async def rename(self, ctx, *, rename = None):
          if rename == None:
               await ctx.send("{0} Please enter a new name for your vc.".format(ctx.author.name))
          else:
               voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
               if voiceChannel != None:
                         await voiceChannel.edit(name=rename)
                         await ctx.send("{0} Your channel's name was changed to {1}".format(ctx.author.name, voiceChannel.mention))
               else:
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
          
          voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
          if voiceChannel != None:
               await voiceChannel.edit(rtc_region=region)
               await ctx.send("{0} Your vc: {1} was set to region {2}".format(ctx.author.name, voiceChannel.mention, text))
          else:
               await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="lock", help="Locks your vc", description="Changes your vc to invite only members can join use t!vc invite <@user> to invite someone")
     async def lock(self, ctx):
          owner = ctx.author.id
          roleList = self.vcRoleRead(ctx)
          voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
          if voiceChannel != None:
               for role in roleList:
                    await voiceChannel.set_permissions(ctx.guild.get_role(role), view_channel=True, read_messages=True, send_messages=False, read_message_history=True, use_voice_activation=True, speak=True, connect=False, reason="{0} locked their vc: {1}".format(ctx.author.name, voiceChannel.name))
               await ctx.send("{0} Your vc: {1} was locked".format(ctx.author.name, voiceChannel.mention))
          else:
               await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="unlock", help="Unlocks your vc", description="All verified members can join your vc if unlocked")
     async def unlock(self, ctx):
          owner = ctx.author.id
          roleList = self.vcRoleRead(ctx)
          voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
          if voiceChannel != None:
               for role in roleList:
                    await voiceChannel.set_permissions(ctx.guild.get_role(role), view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, speak=True, connect=True, reason="{0} unlocked their vc: {1}".format(owner, voiceChannel.name))
               await ctx.send("{0} Your vc: {1} was unlocked".format(ctx.author.name, voiceChannel.mention))
          else:
               await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="invite", usage=" <@user>", help="Invites a user to your vc", description="Allow specified user to join your vc")
     async def invite(self, ctx, user: discord.Member):
          if user == None:
               await ctx.send("Please mention a user to invite.")
          else:
               voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
               if voiceChannel != None:
                    await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, speak=True, connect=True, reason="{0} invited {1} to their vc: {2}".format(user.name, ctx.author.name, voiceChannel.name))
                    await ctx.send("{0} {1} invited you to their vc: {2}".format(user.mention, ctx.author.name, voiceChannel.mention))
               else:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="limit", usage=" <number of users>", help="Sets the limit for how many spots are in vc, use 0 to remove limit")
     async def limit(self, ctx, limit: int = 0):
          voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
          if voiceChannel != None:
               await voiceChannel.edit(user_limit=limit)
               await ctx.send("{2} The user limit in your vc {0} was changed to {1}".format(voiceChannel.mention, limit, ctx.author.name))
          else:
               await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="request", usage="<@user>", help="Sends a user a request to join their vc, request last 5 minutes")
     async def request(self, ctx, user: discord.Member):
          #gets channel for bot message
          if user == None:
               await ctx.send("{0} Please mention a user to request to join".format(ctx.author.name))
          else:
               if user.id == ctx.author.id:
                    await ctx.send("{0} you silly goose! You can't request to join your own vc.".format(ctx.author.name))
               else:
                    dsChannel = self.vcChannelRead(ctx)
                    if ctx.message.channel.id == dsChannel.id:

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
     async def kick(self, ctx, user: discord.Member):
          if user == None:
               await ctx.send("{0} Please mention a user to kick.".format(ctx.author.name))
          else:
               voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
               if voiceChannel != None:
                    await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=False, read_message_history=True, stream=False, use_voice_activation=True, speak=False, connect=False, reason="{0} kicked {1} from their vc: {2}".format(ctx.author.name, user.name, voiceChannel.name))
                    if user.voice != None:
                         if user.voice.channel.id == voiceChannel.id:
                              await user.move_to(None)
                              await ctx.send("{0} was kicked from your vc: {1}".format(user.name, voiceChannel.mention))
               else:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="mute", usage="<@user>", help="Mutes a user inside your vc")
     async def mute(self, ctx, user: discord.Member):
          if user == None:
               await ctx.send("{0} Please mention a user to mute.".format(ctx.author.name))
          else:
               voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
               if voiceChannel != None:
                    await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=False, read_message_history=True, use_voice_activation=True, stream=False, connect=True, speak=False, reason="{0} muted {1} in their vc: {2}".format(ctx.author.name, user.name, voiceChannel.name))
                    if user.voice.channel.id == voiceChannel.idt:
                         await user.move_to(voiceChannel)
                    await ctx.send("{0} was muted in your vc: {1}".format(user.name, voiceChannel.mention))
               else:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="unmute", usage="<@user>", help="Unmutes a user inside your vc")
     async def unmute(self, ctx, user: discord.Member):
          if user == None:
               await ctx.send("{0} Please mention a user to unmute.".format(ctx.author.name))
          else:
               voiceChannel = self.vcOwnerRead(ctx.guild.id, ctx.author.id)
               if voiceChannel != None:
                    await voiceChannel.set_permissions(user, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, stream=True, use_voice_activation=True, connect=True, speak=True, reason="{0} unmuted {1} in their vc: {2}".format(ctx.author.name, user.name, voiceChannel.name))
                    if user.voice.channel.id == voiceChannel.id:
                         await user.move_to(voiceChannel)
                    await ctx.send("{0} was unmuted in your vc: {1}".format(user.name, voiceChannel.mention))
               else:
                    await ctx.send("{0} You have no vc created use t!vc create [Name] to create one.".format(ctx.author.name))

     @vc.command(name="claim", usage="", help="Claims a voice channel from another user if they're not in it.")
     async def claim(self, ctx):
          owner:int = 0
          newOwner = str(ctx.author.id)
          channelid = ctx.author.voice.channel.id
          newWrite = {newOwner : channelid}
          x = None
          vcEmpty = False
          guild = ctx.guild.id
          if channelid != None:
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                    try:
                         x = json.load(vcOwners)
                         for server, vcs in x.items():
                              if server == str(guild):
                                   for i in vcs:
                                        for vcOwnList, vcNameList in i.items():
                                             if int(vcNameList) == int(channelid):
                                                  owner = int(vcOwnList)
                                                  ownerObj = await self.bot.get_or_fetch_member(ctx.guild, owner)
                                                  if ownerObj.voice == None or ownerObj.voice.channel.id != channelid:
                                                       await ctx.send("{0} has claimed {1}".format(ctx.author.mention, self.bot.get_channel(vcNameList).mention))
                                                       await self.bot.get_channel(vcNameList).set_permissions(ctx.author, view_channel=True, read_messages=True, send_messages=True, read_message_history=True, use_voice_activation=True, stream=True, speak=True, connect=True)
                                                       vcEmpty = True
                                                  else:
                                                       await ctx.send("<@{0}> is still in their vc you can only run this when they have left".format(owner))
                              if vcEmpty:
                                   if str(ctx.guild.id) in x:
                                        y = x[str(guild)].copy()
                                        y[0].pop(str(owner), None)
                                        y[0].update(newWrite)
                    except ValueError:
                         await ctx.send("{0} is not a valid channel id for a personal vc.".format(channelid))
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'w') as vcWrite:
                    try:
                         json.dump(x, vcWrite)
                    except ValueError:
                         print("vcOwners.json write failed.")

     @vc.command(name="transfer", usage=" <@user>", help="Transfers a voice channel to another user")
     async def transfer(self, ctx, newOwner:discord.Member):
          owner = str(ctx.author.id)
          if ctx.author.voice != None:
               channelid = ctx.author.voice.channel.id
               newWrite = {str(newOwner.id) : int(channelid)}
               x = None
               vcEmpty = False
               guild = ctx.guild.id
               if channelid != None:
                    with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'r') as vcOwners:
                         try:
                              x = json.load(vcOwners)
                              for server, vcs in x.items():
                                   if server == str(ctx.guild.id):
                                        for i in vcs:
                                             for vcOwnList, vcNameList in i.items():
                                                  if vcOwnList == str(ctx.author.id):
                                                       ownerObj = await self.bot.get_or_fetch_member(ctx.guild, vcOwnList)
                                                       if ownerObj.voice.channel.id == channelid:
                                                            await ctx.send("{0} has transfered vc ownership to {1}".format(ctx.author.mention, self.bot.get_channel(vcNameList).mention))
                                                            vcEmpty = True
                                                       else:
                                                            await ctx.send("<@{0}> you must be in your vc to run this command".format(ctx.author.id))
                              if vcEmpty:
                                   if str(ctx.guild.id) in x:
                                        y = x[str(guild)].copy()
                                        y[0].pop(str(owner), None)
                                        y[0].update(newWrite)
                              else:
                                   await ctx.send("You don't own this voice channel.")
                         except ValueError:
                              await ctx.send("{0} is not a valid channel id for a personal vc.".format(channelid))
                    with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcOwners.json', 'w') as reputationWrite:
                         try:
                              json.dump(x, reputationWrite)
                         except ValueError:
                              print("vcOwners.json write failed.")
          else:
               await ctx.send("You can only run this command while you are in your voice channel.")

     @vc.command(name="setup", help="Set's up a channel for creating custom vc's in, please put this channel in the category you would like all custom vc's to be made in")
     async def setup(self, ctx):
          guild = ctx.guild.id
          run : bool = True
          x : TextIOWrapper
          y : TextIOWrapper
          #make sure server doesn't already have one setup
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcChannels.json', 'r') as vcChannels:
               try:
                    x = json.load(vcChannels)
                    for server, channel in x.items():
                         if server == str(guild):
                              run = False
               except ValueError:
                    run = False
                    print("vcchannel.json failed to read")
          if run:
               #create custom vc command channel
               channel = await ctx.guild.create_text_channel("personal-vc-commands")
               await ctx.send("Make sure to put the personal-vc-commands channel in the category you wish channels to be made in. You may rename the channel to whatever you wish.")
               #save channel id with guild id to be read later
               newWrite = {str(guild) : channel.id}
               x.update(newWrite)
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcChannels.json', 'w') as vcChannelsWrite:
                    try:
                         json.dump(x, vcChannelsWrite)
                    except ValueError:
                         print("vcchannels.json write failed.")
          #ask for public roles that can join channels on creation, these roles will also be used for unlock/lock commands
          mess1 = await ctx.send("Please ping any roles you wish to have permissions to join channels on creation. These roles will also be used for unlock/lock commands. If you wish to allow anyone to join on creation type 'none'.")
          def check(m):
               return m.channel == mess1.channel

          msg = await self.bot.wait_for('message', check=check, timeout=600)

          #save public roles to seperate file with guild id to be read later
          roles = []
          if msg.content != "none":
               for i in msg.role_mentions:
                    roles.append(i.id)
          else:
               roles.append(ctx.guild.id)
          await mess1.delete()
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcRoles.json', 'r') as vcRoles:
               try:
                    y = json.load(vcRoles)
                    y.update({str(guild) : roles})
               except ValueError:
                    print("vcroles.json read failed.")
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcRoles.json', 'w') as vcRolesWrite:
               try:
                    json.dump(y, vcRolesWrite)
               except ValueError:
                    print("vcroles.json write failed.")
               #display settings to insure they are correct
          await ctx.send("Your settings are currently: {0} as the channel and {1} are the public roles that will be used.".format(channel.name, roles))
     @vc.command(name="clear_settings", help="Clears the personal vc commands channel allowing for fresh setup")
     async def clear_settings(self, ctx):
          #deletes vc commands channel from file
          run : bool = False
          run2 : bool = False
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcChannels.json', 'r') as vcChannels:
               try:
                    x = json.load(vcChannels)
                    for server, channel in x.items():
                         if server == str(ctx.guild.id):
                              run = True
               except ValueError:
                    print("vcchannel.json failed to read")
          if run == True:
               x.pop(str(ctx.guild.id), None)
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcChannels.json', 'w') as vcChannelsWrite:
                    try:
                         json.dump(x, vcChannelsWrite)
                    except ValueError:
                         print("vcchannels.json write failed.")
          else:
               await ctx.send("Your server is not setup yet")
          #deletes public roles from file
          with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcRoles.json', 'r') as vcRoles:
               try:
                    y = json.load(vcRoles)
                    for server, channel in y.items():
                         if server == str(ctx.guild.id):
                              run2 = True
               except ValueError:
                    print("vcroles.json read failed.")
          if run2 == True:
               y.pop(str(ctx.guild.id), None)
               with open('/home/discord/.local/share/Red-DiscordBot/data/tpun/cogs/Tpun/vcRoles.json', 'w') as vcRolesWrite:
                    try:
                         json.dump(y, vcRolesWrite)
                    except ValueError:
                         print("vcroles.json write failed.")
          if run and run2:
               await ctx.send("Your server's vc data has been cleared.")

#     @commands.command(name="lewd", help="Unmutes a user inside your vc")
#     async def lewd(self, ctx):
     
#     @commands.command(name="thinking", help="Unmutes a user inside your vc")
#     async def thinking(self, ctx):

#     @commands.command(name="teehee", help="Unmutes a user inside your vc")
#     async def teehee(self, ctx):

#     @commands.command(name="scoff", help="Unmutes a user inside your vc")
#     async def scoff(self, ctx):

#     @commands.command(name="thumbs", help="Unmutes a user inside your vc")
#     async def thumbs(self, ctx):

#     @commands.command(name="grin", help="Unmutes a user inside your vc")
#     async def grin(self, ctx):

     @commands.command(name="smile", help="Unmutes a user inside your vc")
     async def smile(self, ctx):
          url = "https://kawaii.red/api/gif/smile/token=365398642334498816.8rv0PoPGLF9fltJXTq41/"
          response = urllib.request.urlopen(url)
          data = json.loads(response.read())
          await ctx.send(data)

     @commands.command(name="triggered", help="Unmutes a user inside your vc")
     async def triggered(self, ctx):
          url = "https://kawaii.red/api/gif/triggered/token=365398642334498816.8rv0PoPGLF9fltJXTq41/"
          response = urllib.request.urlopen(url)
          data = json.loads(response.read())
          await ctx.send(data)

#     @commands.command(name="wag", help="Unmutes a user inside your vc")
#     async def wag(self, ctx):
          
#     @commands.command(name="suck", usage="<@user>", help="Unmutes a user inside your vc")
#     async def suck(self, ctx, user: discord.Member):

#     @commands.command(name="fuck", usage="<@user>", help="Unmutes a user inside your vc")
#     async def fuck(self, ctx, user: discord.Member):

     @commands.command(name="boop", usage="<@user>", help="Unmutes a user inside your vc")
     async def boop(self, ctx, user: discord.Member):
          url = "https://kawaii.red/api/gif/boop/token=365398642334498816.8rv0PoPGLF9fltJXTq41/"
          response = urllib.request.urlopen(url)
          data = json.loads(response.read())
          await ctx.send(data)

     @commands.command(name="nom", usage="<@user>", help="Unmutes a user inside your vc")
     async def nom(self, ctx, user: discord.Member):
          url = "https://kawaii.red/api/gif/nom/token=365398642334498816.8rv0PoPGLF9fltJXTq41/"
          response = urllib.request.urlopen(url)
          data = json.loads(response.read())
          await ctx.send(data)

#     @commands.command(name="bully", usage="<@user>", help="Unmutes a user inside your vc")
#     async def bully(self, ctx, user: discord.Member):

#     @commands.command(name="snuggle", usage="<@user>", help="Unmutes a user inside your vc")
#     async def snuggle(self, ctx, user: discord.Member):

#     @commands.command(name="handholding", usage="<@user>", help="Unmutes a user inside your vc")
#     async def handholding(self, ctx, user: discord.Member):

#     @commands.command(name="hold", usage="<@user>", help="Unmutes a user inside your vc")
#     async def hold(self, ctx, user: discord.Member):

