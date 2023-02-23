import nextcord
from nextcord.ext import commands
import datetime
import asyncio

intents = nextcord.Intents.default()
intents.message_content = True

discordToken = ''
discordBot = commands.Bot(command_prefix="!", intents=intents)

@discordBot.event
async def on_ready():
    global channel
    global ping_role
    global emojiyes
    global emojino

    print(f"Logged in as: {discordBot.user.name}")
    channel = discordBot.get_channel(1076990299890516128)
    ping_role = nextcord.Guild.get_role(discordBot.get_guild(991826379953950760), 993976653531328564)
    await ScheduleLoop()

async def ScheduleLoop():
    sent = False
    while True:
        if sent == True:
            await asyncio.sleep(datetime.timedelta(days=1).total_seconds())
            sent = False
        await asyncio.sleep(datetime.timedelta(hours=1).total_seconds())

        if datetime.datetime.now().weekday() == 1:
            while sent == False:
                await asyncio.sleep(datetime.timedelta(minutes=10).total_seconds())
                if datetime.datetime.now().hour == 23:
                    await channel.send(f"{ping_role.mention} Vote for extra raids on:")
                    test = await channel.send("Wednesday")
                    await test.add_reaction(":yes~1:")
                    await test.add_reaction(":no~1:")
                    test = await channel.send("Saturday")
                    await test.add_reaction(":yes~1:")
                    await test.add_reaction(":no~1:")
                    test = await channel.send("Sunday")
                    await test.add_reaction(":yes~1:")
                    await test.add_reaction(":no~1:")
                    test = await channel.send("Monday")
                    await test.add_reaction(":yes~1:")
                    await test.add_reaction(":no~1:")
                    sent = True


discordBot.run(discordToken)