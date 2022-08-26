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

    @commands.admin_or_permissions()
    @commands.command(name="pingeveryone")
    async def pingeveryone(self, ctx: commands.Context):
        """
        This command just pings everyone
        """
        allowed_mentions = discord.AllowedMentions(everyone=True)
        await ctx.send(content="@everyone", allowed_mentions=allowed_mentions)

    @commands.admin_or_permissions()
    @commands.command(name="pinghere")
    async def pinghere(self, ctx: commands.Context):
        """
        This command just pings here
        """
        allowed_mentions = discord.AllowedMentions(everyone = True)
        await ctx.send(content="@here", allowed_mentions=allowed_mentions)
