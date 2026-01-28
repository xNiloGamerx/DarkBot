from discord.ext import commands

from api.connection import SupabaseConnection
from api.guild.register_guild import RegisterGuild
from api.member.register_member import RegisterMember

class MemberEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = bot.supabase_connection

    @commands.Cog.listener()
    async def on_member_join(self, member):
        register_member = RegisterMember(self.connection)
        register_member.register_member(member)


async def setup(bot):
    await bot.add_cog(MemberEvents(bot))