from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import requests
import logging
import asyncio
import openai

class ChatGPT(commands.Cog):
  def __init__(self, bot: Red) -> None:
    self.prompt = ""
    self.response = ""
    self.bot = bot
    self.log = logging.getLogger('red.tpun.occupations')
    self.config = Config.get_conf(
        self,
        identifier=365398642334498816
    )
    
  def send_message(self, message):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=self.prompt + message,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5
    )
    self.response = response["choices"][0]["text"]
    return self.response

  @commands.command(name="chatgpt")
  async def chatgpt(self, ctx: commands.Context, *, query: str):
    """
    Asks chatgpt a query
    """
    openai.api_key = await self.bot.get_shared_api_tokens("openai")
    response : str = self.send_message(query)
    ctx.reply(response)
