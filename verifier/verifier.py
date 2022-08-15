from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import asyncio
from redbot.core.utils.menus import start_adding_reactions
import datetime

class verifier(commands.Cog):
    """
    Emoji Verification cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )

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

    @commands.admin()
    @commands.command(name="verify", help="Opens the verification gui")
    async def verify(self, ctx: commands.Context, user: discord.Member):
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