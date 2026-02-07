import json
import discord
from discord import app_commands
from discord.ext import commands

import traceback

from api.counting.counting_user import CountingUser
from api.member.get_member import GetMember
from utils.counting.embeds import Embeds
from utils.privay_policy import PrivacyPolicy

class PrivacyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.get_member = GetMember(self.connection)
        self.counting_user = CountingUser(self.connection)
        self.embeds = Embeds()
        self.privacy_policy = PrivacyPolicy(self.connection)
    
    counting = app_commands.Group(
        name="privacy", 
        description="Commands für Privacy."
    )
    
    @counting.command(name="show", description="Zeigt alle Daten die von dem Bot über dich erhoben werden.")
    async def show(
        self,
        interaction: discord.Interaction
    ):
        try:
            user_data = await self.get_member.get(user_id=interaction.user.id)
            counting_user_data = await self.counting_user.get_or_create(interaction.guild, interaction.user)

            await interaction.response.send_message(
                embed=self.embeds.create_privacy_user_info_embed(interaction.user, user_data, counting_user_data),
                ephemeral=True
            )
        except Exception as e:
            print(f"Error in privacy show command: {e}")
            print(traceback.format_exc())

    @counting.command(name="delete", description="Löscht alle Daten die vom Bot über dich erhoben wurden.")
    async def delete(
        self,
        interaction: discord.Interaction
    ):
        try:
            await self.privacy_policy.delete_user_data(interaction)
        except Exception as e:
            print(f"Error in privacy delete command: {e}")
            print(traceback.format_exc())


async def setup(bot):
    await bot.add_cog(PrivacyCommands(bot))
