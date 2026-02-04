import discord
from discord.ext import commands


class ShopView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Checkpiont kaufen (15.000)", style=discord.ButtonStyle.primary, emoji="🛡️")
    async def buy_checkpoint(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_points = 20_000
        price = 15_000

        if guild_points >= price:
            await interaction.response.send_message(
                f"✅ **Kauf erfolgreich!** Du hast einen Checkpoint für {price:,} Punkte erworben.", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ **Fehler:** Du hast nicht genug Punkte! Dir fehlen {price - guild_points:,} Punkte.", 
                ephemeral=True
            )

class CountingShop:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def open(self, interaction: discord.Interaction):
        try:
            embed = discord.Color.blue()
            embed = discord.Embed(
                title="🏪 Items Shop",
                description="Verpasse nicht deine Chance, dir wertvolle Vorteile zu sichern!",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="🚩 Checkpoint", 
                value="**Preis:** 15.000 Punkte\n**Info:** Speichert deinen Fortschritt im Spiel.", 
                inline=False
            )
            
            embed.set_footer(text="Klicke auf den Button unten zum Kaufen")

            # Senden der Nachricht mit Embed und Button (View)
            await interaction.channel.send(embed=embed, view=ShopView(self.bot))
            await interaction.response.send_message("🛒 Der Shop wurde geöffnet!", ephemeral=True)
        except Exception as e:
            print(f"Error opening shop: {e}")
