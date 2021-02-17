from aiogram import types
from aiogram.utils.exceptions import BadRequest

from config import CHANNEL_USERNAME
from loader import bot
from subfuncs import decorators as current

__all__ = ['is_channel_member']


@current.set_user
async def is_channel_member(channel=CHANNEL_USERNAME, user: types.User = None) -> bool:
    """Check if user is subscribed on channel."""
    try:
        chat_member = await bot.get_chat_member(channel, user.id)
        if chat_member.is_chat_member():
            return True
    except BadRequest:
        pass

    return False
