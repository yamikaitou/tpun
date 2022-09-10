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
import time
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
            "cooldown": ""
        }
        default_guild = {
            "maxsalary": 0,
            "chancescalar": 1.0,
            "timediff": 3600.0
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    async def create_embed(self, jobs: dict):
        description="A list of avalaible jobs below\nThe High the salary the less chance of getting the job"
        embed = discord.Embed(title="Job Board", description=description, color=0xc72327)
        iteration = 1
        p = inflect.engine()
        for title, salary in jobs.items():
            message = "Title: " + title + " \n " + " Salary: " + str(int(salary))
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
        maxsalary = await self.config.guild(ctx.guild).maxsalary()
        chanceScalar = await self.config.guild(ctx.guild).chancescalar()
        jobChance = 1 - ((jobSalary / maxsalary) * chanceScalar)
        roll = random.random()
        if roll <= jobChance: 
            #set that occupation to users job
            await self.config.member(ctx.author).title.set(jobName)
            await self.config.member(ctx.author).salary.set(jobSalary)
            await mess.reply("Congrats you got the job as {0}, your new salary is {1}".format(jobName, jobSalary))
        else:
            await mess.reply("I'm sorry but you didn't qualify for the job. Guess it's back to searching.")
        #start cooldown for job searching
        time_format = '%Y %m %d %H:%M:%S %z'
        utc_zone = tz.gettz('UTC')
        time = datetime.utcnow()
        await self.config.member(ctx.author).cooldown.set(time.strftime(time_format))

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
    async def jobboard(self, ctx: commands.Context):
        """
        Displays the job board with a list of jobs
        """
        #check cooldown for job searching
        cooldown = await self.config.member(ctx.author).cooldown()
        timediff = await self.config.guild(ctx.guild).timediff()
        if cooldown is None:
            cooldown = datetime.utcfromtimestamp(1302872043.0)
        else:
            cooldown = parser.parse(cooldown)
        if cooldown.timestamp() + timediff < datetime.utcnow().timestamp():
            app_id = "1cf735c8"
            api_key = "07f06d440a5df3423f00659899be7bf5"
            #use api to get random jobs, if not possible use List
            response = requests.get("http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={0}&app_key={1}&results_per_page=250&full_time=1&content-type=application/json".format(app_id, api_key))
            jobs = response.json()
            jobResults: list = jobs["results"]
            titleList: dict = {}
            for job in jobResults:
                titleList.update({job["title"]:job["salary_max"]})
            jobList = list(titleList)
            #choose 4 jobs from the list we get back at random
            job1 = jobList[self.random_generator(jobList)]
            job2 = jobList[self.random_generator(jobList)]
            job3 = jobList[self.random_generator(jobList)]
            job4 = jobList[self.random_generator(jobList)]
            titleList = {job1:titleList[job1], job2:titleList[job2], job3:titleList[job3], job4:titleList[job4]}
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
        else:
            await ctx.send("Sorry your job search is on hold, this can take up to 1 hour")

    async def random_generator(jobList):
        return random.randint(0, (len(jobList)-1))

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
        wages = [20000, 40000, 75000, 100000, 125000, 150000]
        chanceScalar = await self.config.guild(ctx.guild).chancescalar()
        message = "The max salary was set to `{0}`".format(salary)
        for wage in wages:
            chance = 100 * (1 - ((wage / salary) * chanceScalar))
            if chance < 0:
                chance = 0
            message = message + "\nThe current chance to get a `{0}` salary job is `{1}%`".format(wage, chance)
        await ctx.reply(message)

    @job.command(name="chancescalar")
    async def chancescalar(self, ctx: commands.Context, scalar: float = 1.0):
        """
        Command for setting the scalar for chances of getting a job

        The closer to 0 the more likely, the higher than 1 the less likely
        """
        await self.config.guild(ctx.guild).chancescalar.set(scalar)
        wages = [20000, 40000, 75000, 100000, 125000, 150000]
        maxsalary = await self.config.guild(ctx.guild).maxsalary()
        message = "The chance scalar was set to `{0}`".format(scalar)
        for wage in wages:
            chance = 100 * (1 - ((wage / maxsalary) * scalar))
            if chance < 0:
                chance = 0
            message = message + "\nThe current chance to get a `{0}` salary job is `{1}%`".format(wage, chance)
            await ctx.reply(message)

    @job.command(name="cooldown")
    async def cooldown(self, ctx: commands.Context, seconds: float = 1.0):
        """
        Command for setting the cooldown
        """
        await self.config.guild(ctx.guild).timediff.set(seconds)
        await ctx.reply("The job search cooldown was set to `{0}` seconds.".format(seconds))
