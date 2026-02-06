import discord
from discord import app_commands
from discord.ext import commands

from api.channel.register_channel import RegisterChannel
from api.counting.register_counting_guild import RegisterCountingGuild
from cogs.counting.shop.counting_shop import CountingShop
from utils.counting.embeds import Embeds

class CountingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.register_channel = RegisterChannel(self.connection)
        self.register_counting_guild = RegisterCountingGuild(self.connection)
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

    @counting.command(name="test_embed", description="Neues Counting embed testen.")
    async def test_embed(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel | None = None    
    ):
        await Embeds.send_new_counting_embed(self.bot, channel or interaction.channel)


async def setup(bot):
    await bot.add_cog(CountingCommands(bot))
