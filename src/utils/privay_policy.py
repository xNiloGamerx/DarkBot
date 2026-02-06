from discord import Member, TextChannel
import discord

from api.member.register_member import RegisterMember
from utils.counting.embeds import Embeds

class AcceptView(discord.ui.View):
    def __init__(self, on_consent, member: discord.Member):
        super().__init__(timeout=None)
        self.on_consent = on_consent
        self.member = member

    @discord.ui.button(label="Ich akzeptiere das diese Daten gespeichert werden", style=discord.ButtonStyle.green, emoji="✅")
    async def get_consens(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_consent(interaction, self.member)

class PrivacyPolicy:
    def __init__(self, connection):
        self.connection = connection
        self.embeds = Embeds()
        self.register_member = RegisterMember(self.connection)
    
    async def counting_consent(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message("Perfekt! Viel Spaß beim Zählen.")
        await self.register_member.register_member(member)

    async def counting_privacy(self, member: Member, channel: TextChannel):
        await member.send(embed=self.embeds.create_register_user_privacy_embed(member, channel), view=AcceptView(self.counting_consent, member))
