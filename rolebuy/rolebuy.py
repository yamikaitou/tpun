from typing import Literal
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core import bank
from redbot.core import data_manager
import discord
import json
import asyncio
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class rolebuy(commands.Cog):
    """
    Cog for buying roles
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )
        global roleListPath
        path = data_manager.cog_data_path(cog_instance=self)
        roleListPath = path / 'roleList.json'
        if roleListPath.exists():
            pass
        else:
            with roleListPath.open("w", encoding="utf-8") as f:
                f.write("{}")

        global roleCostPath
        path = data_manager.cog_data_path(cog_instance=self)
        roleCostPath = path / 'roleCost.json'
        if roleCostPath.exists():
            pass
        else:
            with roleCostPath.open("w", encoding="utf-8") as f:
                f.write("{}")

    def roleListRead(self, guild: int, roleArg: discord.role):
        global roleListRead
        try:
            with open(str(roleListRead), 'r') as roleList:
                x = json.load(roleList)
                for server, rolesList in x.items():
                    if server == str(guild):
                        for i in rolesList:
                            return i
        except ValueError:
            print("roleList.json failed to read")

    def roleListCost(self, guild: int, roleArg: discord.role):
        global roleListCost
        try:
            with open(str(roleListCost), 'r') as roleCost:
                x = json.load(roleCost)
                for server, rolesList in x.items():
                    if server == str(guild):
                        for i in rolesList:
                            for role, cost in i.items():
                                if role == roleArg.id:
                                    return cost
        except ValueError:
            print("roleCost.json failed to read")

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.group(name="rb", help="Base command for all timed ping commands")
    async def rb(self, ctx):
        pass

    @rb.command(name="buy", help="Buys a role for money")
    async def buy(self, ctx: commands.Context, role: discord.Role):
        userAccount: bank.Account = await bank.get_account(ctx.author)
        buyableRoles = self.roleListRead(ctx.guild.id, role)
        if role.id in buyableRoles.items():
            cost = self.roleListCost(role)
            if userAccount.balance >= cost:
                await ctx.author.add_roles(role)
                await bank.set_balance(ctx.author, userAccount.balance-cost)
                await ctx.send("{0} You bought {1} for {2} currency".format(ctx.author.name, role.name, cost))
            else:
                await ctx.send("I'm sorry {0} but you don't have enough to buy {1} it costs {2} currency".format(ctx.author.name, role.name, cost))
        else:
            await ctx.send("Sorry this role is not for sale, run rb list to find out with ones are.")

    @commands.guildowner_or_permissions()
    @rb.command(name="add", usage="<role mention> <cooldown in seconds>", help="Adds a role to the buyable role list")
    async def add(self, ctx: commands.Context, role: discord.Role, cost: int):
        global roleListPath
        guild = ctx.guild.id
        nC = {role.id: cost}
        with open(str(roleListPath), 'r') as roleList:
            try:
                x = json.load(roleList)
                if str(guild) in x:
                    y = x[str(guild)].copy()
                    y[0].update(nC)
                else:
                    x.update({str(guild): [{}]})
                    y = x[str(guild)].copy()
                    y[0].update(nC)
            except ValueError:
                print("roleList.json read failed")
        with open(str(roleListPath), 'w') as roleList:
            try:
                json.dump(x, roleList)
                await ctx.send("{0} was added to the buyable roles list with cost {1} currency".format(role.mention, cost))
            except ValueError:
                print("roleList.json write failed")

    @commands.guildowner_or_permissions()
    @rb.command(name="remove", usage="<role mention>", help="Removes a role from the buyable role list")
    async def remove(self, ctx: commands.Context, role: discord.Role):
        global roleListPath
        guild = ctx.guild.id
        with open(str(roleListPath), 'r') as roleList:
            try:
                x = json.load(roleList)
            except ValueError:
                print("Failed to read to pingList.json")
        with open(str(roleListPath), 'w') as roleList:
            try:
                if str(guild) in x:
                    y = x[str(guild)].copy()
                    y[0].pop(str(role.id), None)
                    json.dump(x, roleList)
                    if x is None:
                        x = {}
            except ValueError:
                print("Failed to write to roleList.json")
        await ctx.send("{0} was removed from the buyable role List".format(role.mention))

    @rb.command(name="list", help="Lists all the timed ping roles for the server")
    async def list(self, ctx: commands.Context):
        global roleListPath
        guild = ctx.guild.id
        roles = ""
        with open(str(roleListPath), 'r') as roleList:
            try:
                x = json.load(roleList)
                if str(guild) in x:
                    y = x[str(guild)].copy()
                    for i in y:
                        for role, cost in i.items():
                            roles = roles + "<@&{0}> with cost of {1} currency \n".format(role, cost)
                    mess1 = await ctx.send(roles)
                    await asyncio.sleep(120)
                    await mess1.delete()
            except ValueError:
                print("Failed to read roleList.json")
