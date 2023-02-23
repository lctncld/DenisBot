import nextcord
from nextcord.ext import commands
from nextcord.utils import find


class SchedulingBot(commands.Bot):
    def __init__(self, guild_id: int, channel_name: str, extra_days: list, reactions: dict,
                 required_reactions_to_schedule: int, ping_role_name: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.guild_id = guild_id
        self.channel_name = channel_name
        self.extra_days = extra_days
        self.reactions = reactions
        self.required_reactions_to_schedule = required_reactions_to_schedule
        self.ping_role_name = ping_role_name

    @property
    def channel(self):
        channel = next(filter(lambda it: it.name == self.channel_name, self.get_all_channels()))
        return self.get_channel(channel.id)

    @property
    def guild(self):
        return self.get_guild(self.guild_id)

    @property
    def ping_role(self):
        return next(filter(lambda it: it.name == self.ping_role_name, self.guild.roles))

    async def on_connect(self):
        print(f"Connected as: {self.user.name}")

    async def ask_for_extra_days(self):
        await self.wait_until_ready()
        # TODO: remove my old messages
        await self.channel.send(f"{self.ping_role.mention} vote for extra raids on:")
        for day in self.extra_days:
            message = await self.channel.send(f"{day}")
            for emoji in self.reactions.values():
                await message.add_reaction(nextcord.PartialEmoji(name=emoji))

    def __should_handle_reaction(self, channel_id, user_id):
        is_scheduling_channel = channel_id == self.channel.id
        my_own_reaction = user_id == self.user.id
        return is_scheduling_channel and not my_own_reaction

    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        if not self.__should_handle_reaction(channel_id=payload.channel_id, user_id=payload.user_id):
            return
        if payload.emoji.name == self.reactions["yes"]:
            await self.handle_yes(payload.message_id)

    async def handle_yes(self, message_id):
        message = await self.channel.fetch_message(message_id)
        if message.content in self.extra_days:
            # probably there is a better way to get reaction count
            yes = find(lambda it: it.emoji == self.reactions["yes"], message.reactions)
            if yes is None:
                return
            if yes.count == self.required_reactions_to_schedule + 1:
                print("It's time to create an event")

    async def on_raw_reaction_remove(self, payload: nextcord.RawReactionActionEvent):
        if not self.__should_handle_reaction(channel_id=payload.channel_id, user_id=payload.user_id):
            return
