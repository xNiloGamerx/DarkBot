import cmd
from discord.ext import commands

from api.connection import SupabaseConnection
from api.guild.register_guild import RegisterGuild
from api.member.register_member import RegisterMember

class Startup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.register_guild = RegisterGuild(self.connection)
        self.register_member = RegisterMember(self.connection)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        print('------')
        print()

        
        # self.register_guild.register_guilds(self.bot.guilds)

        # for guild in self.bot.guilds:
        #     self.register_member.register_members(guild.members)

        
        await self.bot.tree.sync()
        for cmd in self.bot.tree.get_commands():
            print(cmd.name)




async def setup(bot):
    await bot.add_cog(Startup(bot))
