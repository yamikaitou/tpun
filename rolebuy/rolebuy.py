from typing import Literal
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core import bank
from redbot.core import data_manager
import discord
import json
import asyncio
import logging
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class rolebuy(commands.Cog):
    """
    Cog for buying roles
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.log = logging.getLogger('red.tpun.rolebuy')
        self.config = Config.get_conf(
            self,
            identifier=365398642334498816,
            force_registration=True,
        )
        path = data_manager.cog_data_path(cog_instance=self)
        self.roleListPath = path / 'roleList.json'
        if self.roleListPath.exists():
            pass
        else:
            with self.roleListPath.open("w", encoding="utf-8") as f:
                f.write("{}")

    def getRoleList(self):
        try:
            with open(str(self.roleListPath), 'r') as roleList:
                x = json.load(roleList)
                return x
        except ValueError:
            self.log.exception("roleList.json failed to read")
            return None

    def roleListRead(self, guild: int):
        x = self.getRoleList()
        for server, rolesList in x.items():
            if server == str(guild):
                return rolesList[0]

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.group(name="rb")
    async def rb(self, ctx):
        """
        Base command for all timed ping commands
        """
        pass

    @rb.command(name="buy")
    async def buy(self, ctx: commands.Context, role: discord.Role):
        """
        Buys a role for money
        """
        buyableRoles = []
        userAccount: bank.Account = await bank.get_account(ctx.author)
        for roleList, cost in self.roleListRead(ctx.guild.id).items():
            buyableRoles.append(int(roleList))
            if role.id in buyableRoles:
                if userAccount.balance >= cost:
                    await ctx.author.add_roles(role)
                    await bank.set_balance(ctx.author, userAccount.balance - cost)
                    await ctx.send("{0} You bought {1} for {2} currency".format(ctx.author.name, role.name, cost))
                else:
                    await ctx.send("I'm sorry {0} but you don't have enough to buy {1} it costs {2} currency"
                        .format(ctx.author.name, role.name, cost)
                    )
            else:
                await ctx.send("Sorry this role is not for sale, run rb list to find out with ones are.")

    @commands.guildowner_or_permissions()
    @rb.command(name="add")
    async def add(self, ctx: commands.Context, role: discord.Role, cost: int):
        """
        Adds a role to the buyable role list
        """
        guild = ctx.guild.id
        nC = {role.id: cost}
        x = self.getRoleList()
        if str(guild) in x:
            y = x[str(guild)].copy()
            y[0].update(nC)
        else:
            x.update({str(guild): [{}]})
            y = x[str(guild)].copy()
            y[0].update(nC)
        with open(str(self.roleListPath), 'w') as roleList:
            try:
                json.dump(x, roleList)
                await ctx.send("{0} was added to the buyable roles list with cost {1} currency".format(role.mention, cost))
            except ValueError:
                self.log.exception("roleList.json write failed")

    @commands.guildowner_or_permissions()
    @rb.command(name="remove")
    async def remove(self, ctx: commands.Context, role: discord.Role):
        """
        Removes a role from the buyable role list
        """
        guild = ctx.guild.id
        x = self.getRoleList()
        with open(str(self.roleListPath), 'w') as roleList:
            try:
                if str(guild) in x:
                    y = x[str(guild)].copy()
                    y[0].pop(str(role.id), None)
                    json.dump(x, roleList)
                    if x is None:
                        x = {}
            except ValueError:
                self.log.exception("Failed to write to roleList.json")
        await ctx.send("{0} was removed from the buyable role List".format(role.mention))

    @rb.command(name="list")
    async def list(self, ctx: commands.Context):
        """
        Lists all the timed ping roles for the server
        """
        roles = ""
        i = self.roleListRead(ctx.guild.id)
        for role, cost in i.items():
            roles = roles + "<@&{0}> with cost of {1} currency \n".format(role, cost)
        mess1 = await ctx.send(roles)
        await asyncio.sleep(120)
        await mess1.delete()
