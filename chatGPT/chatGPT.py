from redbot.core import data_manager
from redbot.core import commands
from redbot.core import checks
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
    default_global = {
        "model": "text-ada-001"
    }
    default_guild = {
        "channels": [],
        "replyRespond": True
    }
    self.config.register_global(**default_global)
    self.config.register_guild(**default_guild)

  def send_message(self, user_id, message, model):
    if user_id not in self.user_threads:
      self.user_threads[user_id] = ""
    self.prompt = self.user_threads[user_id]
    response = openai.Completion.create(
      engine=model,
      prompt=self.prompt + message,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5
    )
    self.user_threads[user_id] = response["choices"][0]["text"]
    return self.user_threads[user_id]

  async def send_chat(self, ctx: commands.Context, query: str):
    async with ctx.typing():
        model = await self.config.model()
        self.log.info("Sending query: `" + query + "` to chatGPT. With model: " + model)
        chatGPTKey = await self.bot.get_shared_api_tokens("openai")
        if chatGPTKey.get("api_key") is None:
            self.log.error("No api key set.")
            return await ctx.send("The bot owner still needs to set the openai api key using `[p]set api openai  api_key,<api key>. It can be created at: https://beta.openai.com/account/api-keys`")
        openai.api_key = chatGPTKey.get("api_key")
        response: str = self.send_message(ctx.author.id, query, model)
        if len(response) > 0 and len(response) < 2000:
            self.log.info("Response is under 2000 characters and is: `" + response + "`.")
            await ctx.reply(response)
        elif len(response) > 2000:
            self.log.info("Response is over 2000 characters sending as file attachment. Response is: `" + response + "`.")
            with open(str(ctx.author.id) + '.txt', 'w') as f:
                f.write(response)
            with open(str(ctx.author.id) + '.txt', 'r') as f:
                await ctx.send(file=discord.File(f))
                os.remove(f)
        else:
            await ctx.reply("I'm sorry, for some reason chatGPT's response contained nothing, please try sending your query again.")

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    whitelistedChannels: list = await self.config.guild(message.guild).channels()
    replyRespond: bool = await self.config.guild(message.guild).replyRespond()
    query = message.content
    ctx = await self.bot.get_context(message)
    if message.channel.id in whitelistedChannels:
        await self.send_chat(ctx, query)
    elif replyRespond and message.reference is not None:
        if message.reference.cached_message is None:
            # Fetching the message
            channel = await self.bot.get_channel(message.reference.channel_id)
            msg = await channel.fetch_message(message.reference.message_id)
            context: commands.Context = await self.bot.get_context(msg)

        else:
            msg = message.reference.cached_message
            context: commands.Context = await self.bot.get_context(msg)
        if context.author.id == self.bot.user.id:
            await self.send_chat(ctx, query)

  @commands.group(name="chatgpt")
  async def chatgpt(self, ctx: commands.Context):
        """
        Base command for chatgpt related commands
        """
        pass

  @chatgpt.command(name="chat")
  async def chat(self, ctx: commands.Context, *, query: str):
    """
    Asks chatgpt a query
    """
    await self.send_chat(ctx, query)

  @checks.guildowner()
  @chatgpt.command(name="set")
  async def set(self, ctx: commands.Context, setting: str, value: str):
    """
    Changes settings for bot to use

    Use [p]chatgpt set channeladd <channel_id> or [p]chatgpt set channelremove <channel_id> to set up channel whitelist where the bot will respond.
    Use [p]chatgpt set replyRespond <True or False> to enable or disable the bot responding to replies regardless of channel
    """
    if setting == "channeladd":
        channelId = int(value)
        channel = self.bot.get_channel(channelId)
        if channel == None:
            ctx.reply("That channel does not exist or the bot can not see it.")
        elif channel.guild != ctx.guild:
            ctx.reply("That channel isn't in this server...")
        else:
            currentChannels: list = await self.config.guild(ctx.guild).channels()
            newChannels: list = currentChannels.append(channelId)
            await self.config.guild(ctx.guild).channels.set(newChannels)
            await ctx.reply("<#" + channelId + "> is now whitelisted.")

    elif setting == "channelremove":
        currentChannels: list = await self.config.guild(ctx.guild).channels()
        try:
            newChannels = currentChannels.remove(value)
            await self.config.guild(ctx.guild).channels.set(newChannels)
            await ctx.reply("<#" + channelId + "> is no longer whitelisted.")
        except ValueError:
            newChannels = currentChannels
            ctx.reply("That channel was already not in channel list.")

    elif setting == "replyRespond":
        if value == "true" or value == "True" or value == "1":
            await self.config.guild(ctx.guild).replyRespond.set(True)
            await ctx.reply("replyRespond is now set to True")
        elif value == "false" or value == "False" or value == "0":
            await self.config.guild(ctx.guild).replyRespond.set(False)
            await ctx.reply("replyRespond is now set to False")

  @checks.is_owner()
  @chatgpt.command(name="model")
  async def model(self, ctx: commands.Context, model: str):
    """
    Allows the changing of model chatbot is running options are: 0-`text-ada-001` 1-`text-babbage-001` 2-`text-curie-001` 3-`text-davinci-002` 4-`text-davinci-002-render` 5-`text-davinci-003` current-`shows current model`

    For more information on what this means please check out: https://beta.openai.com/docs/models/gpt-3
    """
    if model == "0" or model == "text-ada-001":
        await self.config.model.set("text-ada-001")
        await ctx.reply("The chatbot model is now set to: `text-ada-001`")

    elif model == "1" or model == "text-babbage-001":
        await self.config.model.set("text-babbage-001")
        await ctx.reply("The chatbot model is now set to: `text-babbage-001`")

    elif model == "2" or model == "text-curie-001":
        await self.config.model.set("text-curie-001")
        await ctx.reply("The chatbot model is now set to: `text-curie-001`")

    elif model == "3" or model == "text-davinci-002":
        await self.config.model.set("text-davinci-002")
        await ctx.reply("The chatbot model is now set to: `text-davinci-002`")

    elif model == "4" or model == "text-davinci-002-render":
        await self.config.model.set("text-davinci-002-render")
        await ctx.reply("The chatbot model is now set to: `text-davinci-002-render`")

    elif model == "5" or model == "text-davinci-003":
        await self.config.model.set("text-davinci-003")
        await ctx.reply("The chatbot model is now set to: `text-davinci-003`")

    elif model == "current":
        currentModel = await self.config.model()
        await ctx.reply("The chatbot model is currently set to: " + currentModel)
