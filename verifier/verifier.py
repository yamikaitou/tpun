from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import asyncio
from redbot.core.utils.menus import start_adding_reactions
import datetime
from redbot.core import data_manager
import json
from redbot.core.utils.predicates import ReactionPredicate
import logging


class verifier(commands.Cog):
    """
    Emoji Verification cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.log = logging.getLogger('red.tpun.verifier')
        self.config = Config.get_conf(
            self,
            identifier=365398642334498816,
            force_registration=True,
        )
        path = data_manager.cog_data_path(cog_instance=self)
        self.verifiedRolesPath = path / 'verifiedRoles.json'
        if self.verifiedRolesPath.exists():
            pass
        else:
            with self.verifiedRolesPath.open("w", encoding="utf-8") as f:
                f.write("{}")

    def getRoleList(self):
        try:
            with open(str(self.verifiedRolesPath), 'r') as verifiedList:
                x = json.load(verifiedList)
                return x
        except ValueError:
            self.log.exception("verifiedRoles.json failed to read")
            return None

    def parseRoleList(self, guild):
        x = self.getRoleList()
        for server, items in x.items():
            if server == str(guild):
                return items[0]

    async def emojiVerifier(self, ctx: commands.Context, emoji, mess1, user: discord.Member):
        unverified: int = None
        male: int
        female: int
        nb: int
        i = self.parseRoleList(ctx.guild.id)
        for key, role in i.items():
            if key == "unverified":
                unverified = ctx.guild.get_role(int(role))
            elif key == "male":
                male = ctx.guild.get_role(int(role))
            elif key == "female":
                female = ctx.guild.get_role(int(role))
            elif key == "nb":
                nb = ctx.guild.get_role(int(role))
        role: discord.Role = None
        if emoji == "♂":
            role = male
        elif emoji == "♀":
            role = female
        elif emoji == "💜":
            role = nb
        if unverified in user.roles:
            await user.add_roles(role)
            await user.remove_roles(unverified)
            await ctx.send("User Verified as {0}".format(role.name))
            await mess1.delete()
        elif unverified is None:
            await ctx.send("Server was not setup, please ask the owner to run [p]vsetup")
        else:
            await ctx.send("User is already verified!")
            await mess1.delete()

    def pred(self, emojis, mess1, user: discord.Member):
        return ReactionPredicate.with_emojis(emojis, mess1, user)

    @commands.admin()
    @commands.command(name="verify")
    async def verify(self, ctx: commands.Context, user: discord.Member):
        """
        Opens the verification gui
        """
        description0: str = 'From below please choose the emoji that best identifies your gender'
        embed = discord.Embed(color=0xe02522, title='Verified emoji selector', description=description0)
        embed.set_footer(text="♂ : Male | ♀ : Female|💜 : Non Binary")
        embed.timestamp = datetime.datetime.utcnow()
        mess1 = await ctx.channel.send(embed=embed)
        emojis = ["♂", "♀", "💜"]
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

    @commands.guildowner()
    @commands.command(name="vsetup")
    async def setup(self, ctx: commands.Context):
        """
        Setup command for verify cog
        """
        newWrite: dict = {}
        guild = ctx.guild.id
        try:
            with open(str(self.verifiedRolesPath), 'r') as verifiedList:
                x = json.load(verifiedList)
        except ValueError:
            self.log.exception("verifiedRoles.json failed to read")

        def check(m):
            return m.channel == mess0.channel

        mess0 = await ctx.send("Please input the role for unverified members.")
        msg0 = await self.bot.wait_for('message', check=check, timeout=120)
        if msg0.content != "none":
            for i in msg0.role_mentions:
                newWrite.update({"unverified": i.id})
        await mess0.delete()
        mess1 = await ctx.send("Please input the role for verified males")
        msg1 = await self.bot.wait_for('message', check=check, timeout=120)
        if msg1.content != "none":
            for i in msg1.role_mentions:
                newWrite.update({"male": i.id})
        await mess1.delete()
        mess2 = await ctx.send("Please input the role for verified females")
        msg2 = await self.bot.wait_for('message', check=check, timeout=120)
        if msg2.content != "none":
            for i in msg2.role_mentions:
                newWrite.update({"female": i.id})
        await mess2.delete()
        mess3 = await ctx.send("Please input the role for verified non-binary")
        msg3 = await self.bot.wait_for('message', check=check, timeout=120)
        if msg3.content != "none":
            for i in msg3.role_mentions:
                newWrite.update({"nb": i.id})
        await mess3.delete()
        if str(guild) in x:
            y = x[str(guild)].copy()
            for key, role in newWrite:
                if role in y[0]:
                    y[0].pop(key, None)
            y[0].update(newWrite)
        else:
            y = [newWrite]
            x.update({str(guild): y})
        with open(str(self.verifiedRolesPath), 'w') as verifiedRoles:
            try:
                json.dump(x, verifiedRoles)
            except ValueError:
                self.log.exception("verifierRoles.json write failed.")
