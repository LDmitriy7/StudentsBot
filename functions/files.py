from typing import Tuple

from aiogram import types

from loader import bot

__all__ = ['get_file_obj', 'send_file']


def get_file_obj(msg: types.Message) -> Tuple[str, str]:
    """Return Tuple[file_type, file_id]."""
    if msg.content_type == 'photo':
        file_id = msg.photo[-1].file_id
    elif msg.content_type == 'document':
        file_id = msg.document.file_id
    else:
        raise TypeError('Forbidden file type')
    return msg.content_type, file_id


async def send_file(chat_id: int, file_type: str, file_id: str):
    if file_type == 'photo':
        await bot.send_photo(chat_id, file_id)
    elif file_type == 'document':
        await bot.send_document(chat_id, file_id)
    else:
        raise TypeError('Forbidden file type')
