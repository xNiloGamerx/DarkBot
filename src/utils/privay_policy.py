from discord import Member, TextChannel
import discord

from api.counting.counting_user import CountingUser
from api.member.delete_member import DeleteMember
from api.member.register_member import RegisterMember
from utils.counting.embeds import Embeds

class AcceptView(discord.ui.View):
    def __init__(self, on_consent, member: discord.Member):
        super().__init__(timeout=60.0)
        self.on_consent = on_consent
        self.member = member

    @discord.ui.button(label="Ich akzeptiere das diese Daten gespeichert werden", style=discord.ButtonStyle.green, emoji="✅")
    async def get_consens(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_consent(interaction, self.member)

class DeleteUserDataView(discord.ui.View):
    def __init__(self, on_consent, member: discord.Member | discord.User):
        super().__init__(timeout=60.0)
        self.on_consent = on_consent
        self.member = member

    @discord.ui.button(label="Ich akzeptiere das alle Daten gelöscht werden.", style=discord.ButtonStyle.green, emoji="✅")
    async def get_consens(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_consent(interaction, self.member)

class PrivacyPolicy:
    def __init__(self, connection):
        self.connection = connection
        self.embeds = Embeds()
        self.register_member = RegisterMember(self.connection)
        self.delete_member = DeleteMember(self.connection)
        self.counting_user = CountingUser(self.connection)
    
    async def counting_consent(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(embed=self.embeds.create_success_embed("Perfekt!", "Viel Spaß beim Zählen."))
        await self.register_member.register_member(member)

    async def counting_privacy(self, member: Member, channel: TextChannel):
        await member.send(embed=self.embeds.create_register_user_privacy_embed(member, channel), view=AcceptView(self.counting_consent, member))

    async def delete_user_data_consent(self, interaction: discord.Interaction, member: discord.Member | discord.User):
        await interaction.response.send_message(
            embed=self.embeds.create_success_embed("Deine Daten werden nun gelöscht!", "Zur erneuten Erstellung des Profils einfach eine der Bot Funktionen nutzen."),
            ephemeral=True
        )
        await self.counting_user.delete(interaction.guild, member)
        await self.delete_member.delete(member)

    async def delete_user_data(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=self.embeds.create_warning_embed(
                "Das Löschen der Nutzer Daten hat folgen",
                "Durch das Löschen deiner User Daten geht der gesamte Fortschritt bei allen Bot Funktionen verloren.\nFalls du das möchtest, klicke auf den unten stehenden Button!"
            ),
            view=DeleteUserDataView(self.delete_user_data_consent, interaction.user),
            ephemeral=True
        )
