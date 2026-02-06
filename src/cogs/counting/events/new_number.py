import discord
from discord.ext import commands

from datetime import datetime, timezone

from api.counting.counting_guild import CountingGuild
from api.counting.counting_user import CountingUser
from api.counting.wrong_number import WrongNumber
from api.member.check_if_member_exists import CheckIfMemberExists
from utils.counting.calculation import Calculation
from utils.counting.reactions import Reactions
from utils.counting.validator import Validator
from utils.numbers import Numbers
from utils.privay_policy import PrivacyPolicy

class NewNumber(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.validator = Validator(self.connection)
        self.calculation = Calculation()
        self.counting_user = CountingUser(self.connection)
        self.counting_guild = CountingGuild(self.connection)
        self.wrong_number = WrongNumber(self.connection)
        self.check_if_member_exists = CheckIfMemberExists(self.connection)
        self.privacy_policy = PrivacyPolicy(self.connection)

        self.counting_channel_cache = {}

    async def on_right_number(self, message: discord.Message):
        await Reactions.add_check_mark_reaction(message)

        content = message.content
        author = message.author
        guild = message.guild
        channel = message.channel

        counting_user = await self.counting_user.get_or_create(guild, author)
        counting_guild_data = await self.counting_guild.get(guild)
        print(counting_user)
        print(counting_guild_data)
        try:
            # Daten von Counting user abfragen
            old_avg = counting_user.get("out_avg_count_reaction_time", None)
            count_total = counting_user.get("out_count_total", 0)
            last_counted_at: datetime = datetime.fromisoformat(counting_guild_data.get("out_last_counted_at", None)).astimezone(timezone.utc) if counting_guild_data.get("out_last_counted_at", None) else message.created_at.astimezone(timezone.utc)

            # Reaction Time average berechnen
            last_counted_at_timestamp = last_counted_at.timestamp()
            reaction_time =  message.created_at.astimezone(timezone.utc).timestamp() * 1000 - last_counted_at_timestamp * 1000
            print(reaction_time)
            new_avg = self.calculation.calculate_counting_avg(old_avg, count_total, reaction_time)
            # Punkte anhand der reaction time berechnen
            points = int(Numbers.make_digits_unique(self.calculation.calculate_counting_points(reaction_time)))

            # Neue Werte erstellen und speichern
            new_count_total = count_total + 1
            new_last_counted_at = message.created_at.astimezone(timezone.utc).isoformat()

            await self.counting_user.update(
                counting_user.get("out_id"),
                count_total=new_count_total,
                avg_count_reaction_time=int(new_avg),
                count_points=counting_user.get("out_count_points", 0) + points,
                last_counted_at=new_last_counted_at
            )
            await self.counting_guild.update(
                counting_guild_data.get("out_id"),
                count_points=counting_guild_data.get("out_count_points", 0) + points,
                last_counted_at=new_last_counted_at
            )

            await Reactions.add_points_reaction(message, points)
        except Exception as e:
            print(f"Error in on_right_number calculation: {e}")

    async def on_wrong_number(self, message: discord.Message):
        await Reactions.add_cross_mark_reaction(message)
        
        guild = message.guild

        counting_guild_data = await self.counting_guild.get(guild)

        await self.wrong_number.run(
            counting_guild_data.get("out_id")
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            content = message.content
            if not content.isnumeric():
                return

            print(f"Got message {content} in Channel {message.channel.name}")

            author = message.author
            if author.bot:
                return

            guild = message.guild
            channel = message.channel

            if guild.id not in self.counting_channel_cache:
                if not await self.validator.is_counting_channel(guild, channel):
                    return
                self.counting_channel_cache[guild.id] = channel.id
            else:
                if self.counting_channel_cache[guild.id] != channel.id:
                    return
                
            if not await self.check_if_member_exists.check_if_member_exists(author):
                await message.delete()
                await self.privacy_policy.counting_privacy(author, channel)
                return

            result_new_number = await self.validator.is_new_number(guild, author, int(content))
            if result_new_number:
                await self.on_right_number(message)
            else:
                await self.on_wrong_number(message)
        except Exception as e:
            print(f"Error in on_message: {e}")

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     print(f"Got message {message.content} in Channel {message.channel.name}")
    #     await Reactions.add_check_mark_reaction(message)
    #     await Reactions.add_points_reaction(message, int(message.content))


async def setup(bot):
    await bot.add_cog(NewNumber(bot))
