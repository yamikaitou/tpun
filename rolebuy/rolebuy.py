from typing import Literal
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core import bank
import discord
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

    @commands.command(name="buy", help="Buys a role for money")
    async def buy(self, ctx: commands.Context, role: discord.Role):
        userAccount: bank.Account = await bank.get_account(ctx.author)
        buyableRoles = [970401202019926116, 970401111334879292, 970400980229320754, 970398750440820758, 970398649030934528, 970398560346599474, 970398471624482886, 970397473849892884, 970397345621614624, 970397226629206106, 970396957564604466, 970396864769826866, 970396683940823110, 970396772369309736, 970396437269586011, 970396353953951794, 970396243593404506, 970396015612006411, 970396117550374932, 970395717975801916, 970395636744749096 ]
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

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)
