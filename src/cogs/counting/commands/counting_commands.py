import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime
import traceback

from api.channel.register_channel import RegisterChannel
from api.counting.counting_guild import CountingGuild
from api.counting.counting_user import CountingUser
from api.counting.register_counting_guild import RegisterCountingGuild
from api.member.get_member import GetMember
from cogs.counting.shop.counting_shop import CountingShop
from utils.counting.embeds import Embeds

class CountingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.register_channel = RegisterChannel(self.connection)
        self.register_counting_guild = RegisterCountingGuild(self.connection)
        self.counting_guild = CountingGuild(self.connection)
        self.counting_user = CountingUser(self.connection)
        self.get_member = GetMember(self.connection)
        self.embeds = Embeds()
        self.shop_obj = CountingShop(self.bot)
    
    counting = app_commands.Group(
        name="counting", 
        description="Commands für Couting."
    )
    
    @counting.command(name="create", description="Erstellt ein neues Counting-Spiel in einem/diesem Kanal.")
    @app_commands.describe(channel="Der Channel in dem gezählt werden soll. Standard ist der aktuelle Kanal.")
    async def create(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel | None = None,
        create_info: bool = True
    ):
        selected_channel = channel or interaction.channel

        await interaction.response.send_message(
            content=f"✅  Neues Counting wird im Kanal {selected_channel.mention} erstellt.",
            ephemeral=True
        )
        
        await self.register_channel.register_channel(selected_channel)

        await self.register_counting_guild.register_counting_guild(
            selected_channel.guild,
            selected_channel
        )

        if create_info:
            await Embeds.send_new_counting_embed(self.bot, selected_channel)

    @counting.command(name="shop", description="Öffnet den Counting Shop.")
    async def shop(
        self,
        interaction: discord.Interaction
    ):
        print("1")
        await self.shop_obj.open(interaction)

    @counting.command(name="stats", description="Zeigt die Stats von dir selbst und vom Server an.")
    @app_commands.describe(user="Zeigt die Stats eines betimmten Users", ephemeral="Die Nachricht nur für dich anzeigen lassen. Defaul: Für alle")
    async def stats(
            self,
            interaction: discord.Interaction,
            user: discord.Member = None,
            ephemeral: bool = False
    ):
        try:
            counting_guild_data = await self.counting_guild.get(interaction.guild)
            user_data = await self.get_member.get_by_id(counting_guild_data['out_last_counted_user_id'])
            last_counted_user = await self.bot.fetch_user(user_data["user_id"]) if user_data else "Keiner"
            print(last_counted_user)

            if not counting_guild_data:
                await interaction.response.send_message(embed=self.embeds.create_error_embed("Kein Counting Profil vorhanden!", "Es wurde bis jetzt kein Counting Spiel angelegt, benutze den Befehl `/counting create` um eines zu erstellen!"), ephemeral=True)
                return
            
            embed_guild = self.embeds.create_counting_guild_stats_embed(interaction, counting_guild_data, last_counted_user)


            counting_user_data = await self.counting_user.get_or_create(interaction.guild, user or interaction.user)

            if not counting_user_data:
                embed_user_not_exist = self.embeds.create_error_embed("Der Nutzer existiert nicht!", "Der Nutzer oder du selbst hat bis jetzt kein Profil!")
                await interaction.response.send_message(embeds=[embed_guild, embed_user_not_exist], ephemeral=ephemeral)
                return

            reaction_time = counting_user_data['out_avg_count_reaction_time'] / 1000

            embed_user = self.embeds.create_counting_member_stats_embed(counting_user_data, reaction_time, user)

            await interaction.response.send_message(embeds=[embed_guild, embed_user], ephemeral=ephemeral)
        except Exception as e:
            print(f"Error in counting stats command: {e}")
            print(traceback.format_exc())

    # @counting.command(name="test_embed", description="Neues Counting embed testen.")
    # async def test_embed(
    #     self,
    #     interaction: discord.Interaction,
    #     channel: discord.TextChannel | None = None    
    # ):
    #     await Embeds.send_new_counting_embed(self.bot, channel or interaction.channel)


async def setup(bot):
    await bot.add_cog(CountingCommands(bot))
