from discord import Message
from utils.emoji import Emoji


class Reactions():
    def __init__(self):
        pass
    
    @staticmethod
    async def add_check_mark_reaction(message: Message):
        print(f"Adding check mark reaction to message {message.content}")
        await message.add_reaction(Emoji.WHITE_CHECK_MARK.value)

    @staticmethod
    async def add_cross_mark_reaction(message: Message):
        print(f"Adding cross mark reaction to message {message.content}")
        await message.add_reaction(Emoji.RED_CROSS_MARK.value)
    
    @staticmethod
    async def add_target_reaction(message: Message):
        print(f"Adding target reaction to message {message.content}")
        await message.add_reaction(Emoji.TARGET.value)

    @staticmethod
    async def add_points_reaction(message: Message, points: int):
        try:
            await Reactions.add_target_reaction(message)
            for char in str(points):
                await message.add_reaction(f"{char}{Emoji.NUMBER_EMOJI_SUFFIX.value}")
        except Exception as e:
            print(f"Error in add_points_reaction: {e}")
