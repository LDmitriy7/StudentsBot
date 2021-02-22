"""Contain funcs for work with files."""
from typing import Literal

from aiogram import types

from loader import bot
from aiogram.contrib.currents import SetCurrent

__all__ = ['get_file_tuple', 'send_file', 'send_files']

FileType = Literal['photo', 'document']
FileTuple = tuple[FileType, str]


def get_file_tuple(msg: types.Message) -> FileTuple:
    """Get tuple[file_type, file_id] from msg content."""
    if msg.content_type == 'photo':
        file_id = msg.photo[-1].file_id
    elif msg.content_type == 'document':
        file_id = msg.document.file_id
    else:
        raise TypeError('Forbidden file type')
    return msg.content_type, file_id


async def send_file(chat_id: int, file_type: FileType, file_id: str):
    """Send photo or document to chat."""
    if file_type == 'photo':
        await bot.send_photo(chat_id, file_id)
    elif file_type == 'document':
        await bot.send_document(chat_id, file_id)
    else:
        raise TypeError('Forbidden file type')


@SetCurrent.chat
async def send_files(files: list[FileTuple], title='<b>Файлы к проекту:</b>', *, chat: types.Chat):
    """Send title and photos/documents if provided."""

    if files:
        await bot.send_message(chat.id, title)
        for f in files:
            await send_file(chat.id, *f)
