import aiocron
from schedulingBot import SchedulingBot


class Jobs:
    def __init__(self, bot: SchedulingBot):
        self.bot = bot

        @aiocron.crontab("55 17 * * TUE")
        async def ask_for_extra_days():
            await bot.ask_for_extra_days()
