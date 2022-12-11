from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import logging
import asyncio
import openai
import os

class chatGPT(commands.Cog):
  def __init__(self, bot: Red) -> None:
    self.prompt = ""
    self.response = ""
    self.bot = bot
    self.log = logging.getLogger('red.tpun.chatGPT')
    self.config = Config.get_conf(
        self,
        identifier=365398642334498816
    )
    self.user_threads = {}
    
  def send_message(self, user_id, message):
    if user_id not in self.user_threads:
      self.user_threads[user_id] = ""
    self.prompt = self.user_threads[user_id]
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=self.prompt + message,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5
    )
    self.user_threads[user_id] = response["choices"][0]["text"]
    return self.user_threads[user_id]

  @commands.command(name="chatgpt")
  async def chatgpt(self, ctx: commands.Context, *, query: str):
    """
    Asks chatgpt a query
    """
    async with ctx.typing():
      self.log.info("Sending query: `" + query + "` to chatGPT.")
      chatGPTKey = await self.bot.get_shared_api_tokens("openai")
      if chatGPTKey.get("api_key") is None:
        self.log.error("No api key set.")
        return await ctx.send("The bot owner still needs to set the openai api key using `[p]set api openai  api_key,<api key>. It can be created at: https://beta.openai.com/account/api-keys`")
      openai.api_key = chatGPTKey.get("api_key")
      response : str = self.send_message(ctx.author.id, query)
      if len(response) < 2000:
        self.log.info("Response is under 2000 characters and is: `" + response + "`.")
        await ctx.reply(response)
      else:
        self.log.info("Response is over 2000 characters sending as file attachment. Response is: `" + response + "`.")
        with open(str(ctx.author.id) + '.txt', 'w') as f:
            f.write(response)
        with open(str(ctx.author.id) + '.txt', 'r') as f:
            await ctx.send(file=discord.File(f))
            os.remove(f)
