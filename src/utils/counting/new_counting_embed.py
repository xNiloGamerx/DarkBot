import discord

class NewCountingEmbed:
    def __init__(self):
        pass

    @staticmethod
    async def send_embed(channel: discord.TextChannel):
        try:
            embed = discord.Embed(
                title="Server Info",
                description="Ein schönes Embed",
                color=discord.Color.blue()
            )

            embed.add_field(name="Mitglieder", value="42", inline=True)
            embed.add_field(name="Boost Level", value="3", inline=True)

            embed.set_footer(text="Powered by discord.py")
            embed.set_thumbnail(url=channel.guild.icon.url if channel.guild.icon else None)

            await channel.send(embed=embed)
        except Exception as e:
            print(f"Fehler beim Senden des Embeds: {e}")