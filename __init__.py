import dotenv
import logging
import os

from jobs import Jobs
from schedulingBot import SchedulingBot

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = SchedulingBot(
    guild_id=int(os.environ['GUILD_ID']),
    channel_name='duty',
    extra_days=["Wednesday", "Saturday", "Sunday", "Monday"],
    reactions={
        "yes": "✅",
        "no": "❌",
    },
    required_reactions_to_schedule=1,
    ping_role_name="fucking slaves"
)
Jobs(bot)
bot.run(os.environ['BOT_TOKEN'])
