import discord
from discord.ext import commands

from utils.counting.reactions import Reactions
from utils.counting.validator import Validator

class NewNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.validator = Validator(self.connection)

    async def make_success_message(self, message: discord.Message):
        pass

    async def make_fail_message(self, message: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            print(f"Got message {message.content} in Channel {message.channel.name}")
            
            author = message.author
            if author.bot:
                return
            guild = message.guild
            channel = message.channel

            if not self.validator.is_counting_channel(guild, channel):
                return

            result_new_number = self.validator.is_new_number(guild, author, int(message.content))
            if result_new_number:
                await self.make_success_message(message)
            else:
                await self.make_fail_message(message)
        except Exception as e:
            print(f"Error in on_message: {e}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f"Got message {message.content} in Channel {message.channel.name}")
        await Reactions.add_check_mark_reaction(message)
        await Reactions.add_points_reaction(message, int(message.content))


async def setup(bot):
    await bot.add_cog(NewNumber(bot))
