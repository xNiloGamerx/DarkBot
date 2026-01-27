from discord.ext import commands

from api.connection import SupabaseConnection
from api.guild.register_guild import RegisterGuild
from api.member.register_member import RegisterMember

class Startup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        print('------')
        print()

        connection = SupabaseConnection()._create_connection()

        register_guild = RegisterGuild(connection)
        register_guild.register_guilds(self.bot.guilds)

        register_member = RegisterMember(connection)
        for guild in self.bot.guilds:
            register_member.register_members(guild.members)


async def setup(bot):
    await bot.add_cog(Startup(bot))
