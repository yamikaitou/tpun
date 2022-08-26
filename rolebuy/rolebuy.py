from typing import Literal
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core import bank
import discord
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
            identifier=365398642334498816
        )
        default_guild = {
            "buyableroles": {}
        }
        self.config.register_guild(**default_guild)

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
        buyableRoles = await self.config.guild(ctx.guild).buyableroles()
        userAccount: bank.Account = await bank.get_account(ctx.author)
        if str(role.id) in buyableRoles.keys():
            if userAccount.balance >= buyableRoles[str(role.id)]:
                await ctx.author.add_roles(role)
                await bank.set_balance(ctx.author, userAccount.balance - buyableRoles[str(role.id)])
                await ctx.send("{0} You bought {1} for {2} currency".format(ctx.author.name, role.name, buyableRoles[str(role.id)]))
            else:
                await ctx.send("I'm sorry {0} but you don't have enough to buy {1} it costs {2} currency"
                    .format(ctx.author.name, role.name, buyableRoles[str(role.id)])
                )
        else:
            await ctx.send("Sorry this role is not for sale, run rb list to find out with ones are.")

    @commands.guildowner_or_permissions()
    @rb.command(name="add")
    async def add(self, ctx: commands.Context, role: discord.Role, cost: int):
        """
        Adds a role to the buyable role list
        """
        buyableRoles = await self.config.guild(ctx.guild).buyableroles()
        nC = {str(role.id): cost}
        buyableRoles.update(nC)
        await self.config.guild(ctx.guild).buyableroles.set(buyableRoles)
        await ctx.send("{0} was added to the buyable roles list with cost {1} currency".format(role.mention, cost))

    @commands.guildowner_or_permissions()
    @rb.command(name="remove")
    async def remove(self, ctx: commands.Context, role: discord.Role):
        """
        Removes a role from the buyable role list
        """
        buyableRoles = await self.config.guild(ctx.guild).buyableroles()
        if str(role.id) in buyableRoles.keys():
            buyableRoles.pop(str(role.id), None)
            await self.config.guild(ctx.guild).buyableroles.set(buyableRoles)
            await ctx.send("{0} was removed from the buyable role List".format(role.mention))
        else:
            await ctx.send("That role isn't a buyable role")

    @rb.command(name="list")
    async def list(self, ctx: commands.Context):
        """
        Lists all the timed ping roles for the server
        """
        roles = ""
        i = await self.config.guild(ctx.guild).buyableroles()
        for role, cost in i.items():
            roles = roles + "<@&{0}> with cost of {1} currency \n".format(role, cost)
        if roles != "":
            mess1 = await ctx.send(roles)
        else:
            mess1 = await ctx.send("There are no buyable roles set up yet")
        await asyncio.sleep(120)
        await mess1.delete()
