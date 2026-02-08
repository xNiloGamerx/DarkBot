from datetime import datetime

import discord
from discord.ext import commands
from discord.utils import format_dt

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
    def create_warning_embed(title, message, footer_text=None):
        # Farbe: Ein schönes Grün (Green 0x2ecc71)
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=message,
            color=0xffa500,
            timestamp=datetime.now()
        )
    
        if footer_text:
            embed.set_footer(text=footer_text)
        else:
            embed.set_footer(text="Warnung, bitte die Nachricht lesen")
            
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
    
    @staticmethod
    def create_register_user_privacy_embed(member: discord.Member, counting_channel: discord.TextChannel):
        embed = discord.Embed(
            title="🛡️ DarkBot | Dateneinsicht",
            description=(
                "Gemäß der DSGVO zeigen wir dir hier transparent an, welche Daten "
                "wir von dir erfassen, um die Funktionen des Bots bereitzustellen.\n\n"
                "Die erhobenen Daten dienen der Übersichtlichkeit des Bots und zur Speicherung von Stats über dein Zählen im Counting des Servers\n\n"
                "Klicke unten zu akzeptieren um die Speicherung der Daten zu akzeptieren\n"
                f"Anschließend kannst du im Counting channel {counting_channel.mention} zählen\n\n"
                "**Daten zur speicherung:**"
            ),
            color=discord.Color.dark_blue(),
            timestamp=datetime.now()
        )

        # Profilbild des Nutzers als Thumbnail oben rechts
        embed.set_thumbnail(url=member.display_avatar.url)

        # Datenfelder hinzufügen
        embed.add_field(name="🆔 Discord User ID", value=f"`{member.id}`", inline=False)
        embed.add_field(name="👤 Username", value=f"{member.name}", inline=True)
        embed.add_field(name="📛 Server-Nickname", value=f"{member.display_name}", inline=False)
        created_str = member.created_at.strftime("%d.%m.%Y um %H:%M Uhr")
        embed.add_field(name="📅 Account erstellt am", value=created_str, inline=True)
        embed.add_field(name="🟢 Ob dein Nutzer Profil im DarkBot System aktiv ist oder nicht", value=f"`true/false`", inline=False)

        return embed

    @staticmethod
    def create_privacy_user_info_embed(user: discord.Member, user_data: dict, counting_user_data: dict):
        combined_data = {**user_data, **counting_user_data}

        lines = [
            f"**{key.replace('out_', '').replace('_', ' ').title()}**: `{value}`" 
            for key, value in combined_data.items()
        ]

        embed = discord.Embed(
            title="👤 Nutzer-Datenblatt",
            description=(
                f"Übersicht über die erhobenen Daten von  {user.mention}"
            ),
            color=0x5865f2
        )

        embed.set_thumbnail(url=user.display_avatar.url)

        embed.add_field(
            name="🆔 Account-Info",
            value="\n".join(lines)
        )

        return embed
        
    @staticmethod
    def create_counting_guild_stats_embed(interaction: discord.Interaction, counting_guild_data: dict, last_counted_user: discord.Member | str):
        last_counted_at_time = datetime.fromisoformat(counting_guild_data['out_last_counted_at']) if counting_guild_data['out_last_counted_at'] else "Nie"

        embed = discord.Embed(
            title="📊 Server Statistiken",
            description=f"Statistiken für Server {interaction.guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(name="🔢 Letzte Zahl", value=f"**{counting_guild_data['out_last_counted_number']}**", inline=True)
        embed.add_field(name="🏆 Punkte", value=f"**{counting_guild_data['out_count_points']}**", inline=True)
        embed.add_field(name="📍 Checkpoint", value=f"**{counting_guild_data['out_count_checkpoint']}**", inline=True)
        embed.add_field(name="👤 Letzter User", value=f"{last_counted_user if isinstance(last_counted_user, str) else last_counted_user.mention}", inline=True)
        embed.add_field(name="🕑 Zuletzt gezählt", value=f"{last_counted_at_time if isinstance(last_counted_at_time, str) else format_dt(last_counted_at_time, style="R")}", inline=True)

        return embed
    
    @staticmethod
    def create_counting_member_stats_embed(counting_user_data, reaction_time, user):
        embed_user = discord.Embed(
            title="👤 User Zähler-Profil",
            description=f"Profil-Details für **{user.mention if user else "dich"}**",
            color=discord.Color.gold()
        )
        embed_user.add_field(name="📈 Gesamt gezählt", value=f"**{counting_user_data['out_count_total']}**", inline=True)
        embed_user.add_field(name="✅ Richtig", value=f"**{counting_user_data['out_count_total'] - counting_user_data['out_count_errors']}**", inline=True)
        embed_user.add_field(name="❌ Fehler", value=f"**{counting_user_data['out_count_errors']}**", inline=True)
        embed_user.add_field(name="💎 Punkte", value=f"**{counting_user_data['out_count_points']}**", inline=True)
        embed_user.add_field(name="⚡ Ø Reaktionszeit", value=f"**{reaction_time:,.0f}s**", inline=False)
        embed_user.set_footer(text=f"")

        return embed_user
