import discord
from discord.ext import commands

import json

from api.counting.counting_guild import CountingGuild
from api.counting.shop import Shop
from utils.counting.embeds import Embeds


class ShopView(discord.ui.View):
    def __init__(self, counting_guild_data: dict, shop_items: dict, functions_map):
        super().__init__(timeout=None)
        self.counting_guild_data = counting_guild_data
        self.shop_items = shop_items
        self.embeds = Embeds()
        self.functions_map = functions_map
        
        for shop_item in self.shop_items["items"]:
            button = discord.ui.Button(
                label=f"{shop_item["name"]} kaufen ({shop_item["price_label"]})",
                style=discord.ButtonStyle.primary,
                emoji=shop_item["emoji"],
                custom_id=f"shop_item_{shop_item["name"]}"
            )

            button.callback = self.create_callback(counting_guild_data, shop_item)

            self.add_item(button)

    def create_callback(self, counting_guild_data, shop_item):
        async def callback(interaction: discord.Interaction):
            await self.functions_map[shop_item["name"]](interaction, shop_item, counting_guild_data)
        return callback

    # @discord.ui.button(label="Checkpoint kaufen (15.000)", style=discord.ButtonStyle.primary, emoji="🛡️")
    # async def buy_checkpoint(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     guild_points = self.counting_guild_data.get("out_count_points", 0)
    #     price = 15_000

    #     if guild_points >= price:
    #         await interaction.response.send_message(
    #             f"✅ **Kauf erfolgreich!** Du hast einen Checkpoint für {price:,} Punkte erworben.", 
    #             ephemeral=True
    #         )
    #     else:
    #         await interaction.response.send_message(
    #             f"❌ **Fehler:** Du hast nicht genug Punkte! Dir fehlen {price - guild_points:,} Punkte.", 
    #             ephemeral=True
    #         )

class CountingShop:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connection = bot.supabase_connection
        self.shop_api = Shop(self.connection)
        self.counting_guild = CountingGuild(self.connection)
        self.embeds = Embeds()
        self.functions_map = {
            "Checkpoint": self.buy_checkpoint
        }

    async def open(self, interaction: discord.Interaction):
        try:
            print("2")
            counting_guild_data = await self.counting_guild.get(interaction.guild)
            if not counting_guild_data:
                await interaction.response.send_message(embed=self.embeds.create_error_embed("Fehler beim öffnen des Shops", "Bitte probiere es gleich noch mal. (Möglicherweise hat dieser Server kein Counting Profil)"), ephemeral=True)
                return
            
            with open("./cogs/counting/shop/counting_shop_items.json", "r", encoding="utf-8") as file:
                shop_items = json.load(file)

            print("3")
            embed = discord.Embed(
                title="🏪 Items Shop",
                description=f"Verpasse nicht deine Chance, dir wertvolle Vorteile zu sichern!\n\n**💰 GILDEN-GUTHABEN**\n> `{counting_guild_data["out_count_points"]} Punkte` (Kann abweichen)",
                color=discord.Color.gold()
            )
            
            print("4")
            for i in range(len(shop_items["items"])):
                shop_item = shop_items["items"][i]
                inline = i % 4 < 2
                embed.add_field(
                    name=f"{shop_item["emoji"]} GEGENSTAND: {shop_item["name"].upper()}", 
                    value=f"> **Preis:** `{shop_item["price_label"]} Punkte`\n> **Info:** {shop_item["description"]}", 
                    inline=inline
                )

            print("5")
            embed.add_field(
                name="",
                value="*Klicke auf den Button unten zum Kaufen*",
                inline=False
            )
            
            print("6")
            embed.set_footer(text=f"Counting Shop • {self.bot.user.name}#{self.bot.user.discriminator}")

            print("7")
            await interaction.channel.send(embed=embed, view=ShopView(counting_guild_data, shop_items, self.functions_map))
            print("8")
            await interaction.response.send_message("🛒 Der Shop wurde geöffnet!", ephemeral=True)
        except Exception as e:
            print(f"Error opening shop: {e}")

    async def buy_checkpoint(self, interaction: discord.Interaction, shop_item, counting_guild_data):
        try:
            print(f"Buying Checkpoint for counting guild: {counting_guild_data["out_guild_id"]} ({counting_guild_data["out_id"]})")
            
            result = await self.shop_api.buy_checkpoint(counting_guild_data["out_id"], shop_item["price"])

            if result["result"]:
                await interaction.response.send_message(
                    embed=self.embeds.create_success_embed(f"{shop_item["name"]} wurde gekauft!", f"{shop_item["name"]} wurde für **{shop_item["price_label"]}** Points von **{interaction.user.mention}** gekauft!")   
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds.create_error_embed(f"{shop_item["name"]} für **{shop_item["price_label"]}** Points konnte **nicht** gekauft werden", result["message"]),
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error in buying Checkpoint: {e}")
