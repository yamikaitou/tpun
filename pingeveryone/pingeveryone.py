from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord


class pingeveryone(commands.Cog):
    """
    Ping Everyone Cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )

    @commands.admin_or_permissions()
    @commands.command(name="pingeveryone", help="This command just ping everyone")
    async def pingeveryone(self, ctx: commands.Context,):
        guild: discord.Guild = ctx.guild
        roles = guild.fetch_roles()
        for role in roles:
            print(role.name)
            if role.name == "everyone":
                await ctx.send(role.mention)
