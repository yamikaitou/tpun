from redbot.core import data_manager
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core import bank
import discord
import requests
import logging
import random
import inflect
import asyncio
from datetime import datetime
from dateutil import tz, parser
import time


class occupations(commands.Cog):
    """
    Adds Occupations that server members can choose from a job board. Members earn money based on their job by spending time in vc
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.log = logging.getLogger('red.tpun.occupations')
        self.config = Config.get_conf(
            self,
            identifier=365398642334498816
        )
        default_global = {
            "title": "",
            "salary": 0.0,
            "vcstarttime": "",
        }
        default_guild = {
            "maxsalary": 0,
            "chancescalar": 1.0
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

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
        jobList = list(jobDict)[:4]
        jobName = ""
        jobSalary = ""
        if emoji == "1️⃣":
            jobName = jobList[0]
            jobSalary = jobs[jobList[0]]
        elif emoji == "2️⃣":
            jobName = jobList[1]
            jobSalary = jobs[jobList[1]]
        elif emoji == "3️⃣":
            jobName = jobList[2]
            jobSalary = jobs[jobList[2]]
        elif emoji == "4️⃣":
            jobName = jobList[3]
            jobSalary = jobs[jobList[3]]
        #Add chance of failing to get job perentage based on salary
        maxsalary = self.config.guild(ctx.guild).maxsalary()
        chanceScalar = self.config.guild(ctx.guild).chancescalar()
        jobChance = 1 - ((jobSalary / maxsalary) * chanceScalar)
        roll = random.random()
        if roll <= jobChance: 
            #set that occupation to users job
            await self.config.member(ctx.author).title.set(jobName)
            await self.config.member(ctx.author).salary.set(jobSalary)
            await mess.reply("Congrats you got the job as {0}, your new salary is {1}".format(jobName, jobSalary))
        else:
            await mess.reply("I'm sorry but you didn't qualify for the job. Guess it's back to searching.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        time_format = '%Y %m %d %H:%M:%S %z'
        utc_zone = tz.gettz('UTC')
        if before.channel is None and after.channel is not None:
            #start a timer for how long user is in vc
            time = datetime.utcnow()
            starttimestr = time.strftime(time_format)
            await self.config.member(member).vcstarttime.set(starttimestr)
        elif before.channel is not None and after.channel is None:
            #end the time for how long the user was in vc
            endtime = datetime.utcnow()
            starttimestr = await self.config.member(member).vcstarttime()
            starttime = parser.parse(starttimestr)
            secondsInVc = (endtime - starttime).total_seconds()
            #pay user based on how long they were in vc
            salary = await self.config.member(member).salary()
            pay = int(((secondsInVc / (60*60*24*30)) * int(salary) * 100) * 0.27)
            self.log.info("{0} was paid {1} for being in vc for {2} minutes".format(member.display_name, str(pay), (secondsInVc/60)))
            await bank.deposit_credits(member, pay)
        else:
            self.log.warn("Something went wrong in on_voice_update")


    @commands.group(name="job")
    async def job(self, ctx: commands.Context):
        """
        Base command for occupation related commands
        """
        pass

    @job.command(name="board")
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
            response = requests.get("http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={0}&app_key={1}&results_per_page=250&full_time=1&content-type=application/json".format(app_id, api_key, search))
            jobs = response.json()
            jobResults: list = jobs["results"]
            titleList: dict = {}
            for job in jobResults:
                titleList.update({job["title"]:job["salary_max"]})
            job1 = random.randint(0, 250)
            job2 = random.randint(0, 250)
            job3 = random.randint(0, 250)
            job4 = random.randint(0, 250)
            jobList = list(titleList)
            len(jobList)
            job1 = jobList[job1]
            job2 = jobList[job1]
            job3 = jobList[job1]
            job4 = jobList[job1]
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

    @job.command(name="current")
    async def currentjob(self, ctx: commands.Context):
        """
        Displays the user's current job
        """
        title = await self.config.member(ctx.author).title()
        salary = await self.config.member(ctx.author).salary()
        if title != None:
            await ctx.reply("Your current job is {0} and your salary is {1}".format(title, str(salary)))
        else:
            await ctx.reply("You do not have a job yet.")

    @job.command(name="quit")
    async def quitjob(self, ctx: commands.Context):
        """
        Quits your current job
        """
        await self.config.member(ctx.author).title.set(None)
        await self.config.member(ctx.author).salary.set(None)
        await ctx.reply("You quit your job. Better search for a new one soon...")

    @job.command(name="maxsalary")
    async def maxsalary(self, ctx: commands.Context, salary: int = 10000):
        """
        Command for setting the max salary
        """
        await self.config.guild(ctx.guild).maxsalary.set(salary)
        await ctx.reply("The max salary was set to {0}".format(salary))

    @job.command(name="chancescalar")
    async def chancescalar(self, ctx: commands.Context, scalar: float = 1.0):
        """
        Command for setting the scalar for chances of getting a job

        The closer to 0 the more likely, the higher than 1 the less likely
        """
        await self.config.guild(ctx.guild).chancescalar.set(scalar)
        await ctx.reply("The chance scalar was set to {0}".format(scalar))