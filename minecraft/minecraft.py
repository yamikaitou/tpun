from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
from mcstatus import MinecraftServer

class pvc(commands.Cog):
    """
    Minecraft cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )
    
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
