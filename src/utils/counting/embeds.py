from datetime import datetime
import discord

from discord.ext import commands

class Embeds:
    def __init__(self):
        pass

    @staticmethod
    async def send_new_counting_embed(bot: commands.Bot, channel: discord.TextChannel):
        try:
            embed = discord.Embed(
                title="🔢 Counting wurde im Channel gestartet",
                description="Ab jetzt kann jeder im <#1466161855335497892>-Channel zählen.\nDer erste Nutzer muss eine **1** schreiben um loszulegen!\nViel Spaß und viel Erfolg! 🍀\n\n",
                color=discord.Color.blue()
            )

            embed.set_author(
                name=f"{bot.user.name}#{bot.user.discriminator}",
                icon_url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url
            )

            embed.add_field(
                name="📜 Die Spielregeln",
                value=
                "• **Abwechselnd zählen:** Du darfst nicht zweimal hintereinander eine Zahl schreiben.\n• **Text ist erlaubt:** Zwischen den Zahlen kann text geschrieben werden.\n• **Konzentration:** Ein Fehler und es wird beim letzten Checkpoint neu gestartet!",
                inline=False
            )

            embed.add_field(
                name="⚡ Speed-Bonus",
                value="Je **schneller** du reagierst, desto **mehr Punkte** gibt es!",
                inline=True
            )

            embed.add_field(
                name="🛡️ Checkpoints",
                value=
                "Nutze deine Punkte, um Checkpoints zu kaufen und euren Fortschritt zu sichern.\nDer Checkpoint ist am Anfang bei **0**."
            )

            embed.set_footer(text=f"Counting • {bot.user.name}#{bot.user.discriminator}")

            await channel.send(embed=embed)
        except Exception as e:
            print(f"Fehler beim Senden des Embeds: {e}")

    @staticmethod
    def create_success_embed(title, message, footer_text=None):
        # Farbe: Ein schönes Grün (Green 0x2ecc71)
        embed = discord.Embed(
            title=f"✅ {title}",
            description=message,
            color=0x2ecc71,
            timestamp=datetime.now()
        )
    
        if footer_text:
            embed.set_footer(text=footer_text)
        else:
            embed.set_footer(text="Aktion erfolgreich ausgeführt")
            
        return embed

    @staticmethod
    def create_error_embed(error_title, error_message, command_name=None):
        # Farbe: Ein kräftiges Rot (Red 0xe74c3c)
        embed = discord.Embed(
            title=f"❌ Fehler: {error_title}",
            description=error_message,
            color=0xe74c3c,
            timestamp=datetime.now()
        )
        
        if command_name:
            embed.add_field(name="Befehl", value=f"`/{command_name}`", inline=True)
        
        embed.set_footer(text="Falls das öfter passiert, kontaktiere bitte @xxnilogamerxx.")
        
        return embed