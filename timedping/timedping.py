from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import time
import asyncio
global tempo
tempo : int = 0

class timedping(commands.Cog):
    """
    Timed Ping cog
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=None,
            force_registration=True,
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        global tempo
        if "@vc ping" in message.content or "@vcping" in message.content or "@VC ping" in message.content:
            if tempo > time.time():
                await message.reply("There is a 5 hour cooldown in between vc ping uses. There is <t:{0}:R> remaining in the cooldown".format(int(tempo)))
            else:
                if message.author.voice != None:
                    await message.reply("<@&931995861779644547>")
                    tempo = time.time() + 18000
                else:
                    await message.reply("You must be in a vc to use the vc ping")