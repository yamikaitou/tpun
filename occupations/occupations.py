from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import requests
import logging


class occupations(commands.Cog):
    """
    Adds Occupations that server members can choose from a job board. Members earn money based on their job by spending time in vc
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self

    @commands.command(name="jobboard")
    async def jobboard(self, ctx: commands.Context, *, search: str = ""):
        """
        Displays the job board with a list of jobs
        """
        app_id = "1cf735c8"
        api_key = "07f06d440a5df3423f00659899be7bf5"
        #use api to get random jobs, if not possible use List
        if search != "":
            response = requests.get("http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={0}&app_key={1}&results_per_page=20&what={2}&full_time=1&content-type=application/json".format(app_id, api_key, search))
            print(response.json())
        else:
            #response = requests.get("http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={0}&app_key={1}&results_per_page=20&what={2}&full_time=1&content-type=application/json".format(app_id, api_key, search))
            await ctx.send("Please include search terms")
        #display 4 jobs in an embed
        #wait for user to emoji react to choose one
        #set that occupation to users job
