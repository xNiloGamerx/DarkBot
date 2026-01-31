import discord
from discord.ext import commands

from cogs.counting.utils.validator import Validator

class NewNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.validator = Validator(self.connection)
        

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            print(f"Got message {message.content} in Channel {message.channel.name}")
        
            guild = message.guild
            channel = message.channel

            if not self.validator.is_counting_channel(guild, channel):
                return

            result_new_number = self.validator.is_new_number(guild, channel, int(message.content))
            print(f"Result of is_new_number: {result_new_number}")
        except Exception as e:
            print(f"Error in on_message: {e}")


async def setup(bot):
    await bot.add_cog(NewNumber(bot))
