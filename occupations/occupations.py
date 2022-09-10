from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
import discord
import requests
import logging
import random
import inflect
import asyncio


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
            message = "Title: " + title + " \n " + " Salary: " + str(salary)
            embed.add_field(name=":{0}:".format(p.number_to_words(iteration)), value=message, inline=False)
            iteration = iteration + 1
        return embed

    def pred(self, emojis, mess, user: discord.Member):
        return ReactionPredicate.with_emojis(emojis, mess, user)

    async def jobChooser(self, ctx: commands.Context, emoji, mess: discord.Message, jobs: dict):
        jobDict = jobs.keys()
        jobList = list(jobDict)[:10]
        jobName = ""
        jobSalary = ""
        if emoji == "1️⃣":
            jobName = jobList[0]
            jobSalary = jobList[jobList[0]]
        elif emoji == "2️⃣":
            jobName = jobList[0]
            jobSalary = jobList[jobList[0]]
        elif emoji == "3️⃣":
            jobName = jobList[0]
            jobSalary = jobList[jobList[0]]
        elif emoji == "4️⃣":
            jobName = jobList[0]
            jobSalary = jobList[jobList[0]]
        #Add chance of failing to get job perentage based on salary

        #Write Chosen job to config

        await mess.reply("You chose {0} as your job, your new salary is {1}".format(jobName, jobSalary))

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
        else:
            #response = requests.get("http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={0}&app_key={1}&results_per_page=20&what={2}&full_time=1&content-type=application/json".format(app_id, api_key, search))
            await ctx.send("Please include search terms")
        #display 4 jobs in an embed
        embed = await self.create_embed(titleList)
        mess = await ctx.send(embed=embed)
        #wait for user to emoji react to choose one
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        start_adding_reactions(mess, emojis)
        try:
            result = await ctx.bot.wait_for("reaction_add", timeout=300.0, check=self.pred(emojis, mess, ctx.author))
            emoji = str(result[0])
            await self.jobChooser(ctx, emoji, mess, titleList)
        except asyncio.TimeoutError:
            await ctx.send('This request timed out.')
            await mess.delete()
        else:
            pass
        #set that occupation to users job
