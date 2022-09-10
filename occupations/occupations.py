from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord
import requests
import logging
import random
import inflect


class occupations(commands.Cog):
    """
    Adds Occupations that server members can choose from a job board. Members earn money based on their job by spending time in vc
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self

    async def create_embed(self, jobs: dict):
        embed = discord.Embed(title="Job Board", description="A list of avalaible jobs below", color=0xc72327)
        iteration = 1
        p = inflect.engine()
        for title, salary in jobs.items():
            message = "Title: " + title + " " + " ⌇ " + " Salary: " + str(salary)
            embed.add_field(name=":{0}:".format(p.number_to_words(iteration)), value=message, inline=True)
            iteration = iteration + 1
        return embed

    @commands.command(name="jobboard")
    async def jobboard(self, ctx: commands.Context, *, search: str = ""):
        """
        Displays the job board with a list of jobs
        """
        app_id = "1cf735c8"
        api_key = "07f06d440a5df3423f00659899be7bf5"
        #use api to get random jobs, if not possible use List
        if search != "":
            response = requests.get("http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={0}&app_key={1}&results_per_page=4&what={2}&full_time=1&content-type=application/json".format(app_id, api_key, search))
            jobs = response.json()
            jobResults: list = jobs["results"]
            titleList: dict = {}
            for job in jobResults:
                titleList.update({job["title"]:job["salary_max"]})
            embed = await self.create_embed(titleList)
            await ctx.send(embed=embed)
        else:
            #response = requests.get("http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={0}&app_key={1}&results_per_page=20&what={2}&full_time=1&content-type=application/json".format(app_id, api_key, search))
            await ctx.send("Please include search terms")
        #display 4 jobs in an embed

        #wait for user to emoji react to choose one
        ranNum :int = random.randrange(0, 9)
        jobDict = titleList.keys()
        #set that occupation to users job
