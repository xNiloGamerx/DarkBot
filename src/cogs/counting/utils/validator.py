from discord import Guild, TextChannel
from api.connection import SupabaseConnection
from api.counting.check_new_number import CheckNewNumber
from api.counting.is_counting_channel import IsCountingChannel


class Validator:
    def __init__(self, connection: SupabaseConnection):
        self.connection = connection
        self.is_counting_channel_api = IsCountingChannel(connection)
        self.checkNewNumber = CheckNewNumber(self.connection)

    def is_counting_channel(self, guild: Guild, channel: TextChannel) -> bool:
        """Überprüft, ob der gegebene Kanal ein Counting-Kanal ist.

        Args:
            guild_id (int): Die ID der Gilde.
            channel_id (int): Die ID des Kanals.

        Returns:
            bool: True, wenn der Kanal ein Counting-Kanal ist, sonst False.
        """
        return self.is_counting_channel_api.is_counting_channel(guild, channel)
    
    def is_new_number(self, guild: Guild, channel: TextChannel, counted_number: int) -> bool:
        """Überprüft, ob die gezählte Zahl korrekt ist.

        Args:
            guild_id (int): Die ID der Gilde.
            channel_id (int): Die ID des Kanals.
            counted_number (int): Die gezählte Zahl.
        """
        return self.checkNewNumber.check_new_number(guild, channel, counted_number)