"""Handle commands "Отменить", "Назад" and query for deleting bound message."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import keyboards as KB
import texts
from data_types import TextQueries
from loader import dp


@dp.message_handler(text='/start', state='*', chat_type='private')
async def send_welcome():
    return UpdateData(new_state='exit'), QuestText(texts.welcome, KB.Main)


@dp.message_handler(text=KB.CANCEL, state='*')
@dp.message_handler(commands='cancel', state='*')
async def cancel(chat_type: str):
    keyboard = KB.Main if chat_type == 'private' else None
    return UpdateData(new_state='exit'), QuestText('Отменено', keyboard)


@dp.message_handler(text=KB.BACK, state='*')
async def go_back():
    on_conv_exit = QuestText('Отменено', KB.Main)
    return UpdateData(new_state='previous', on_conv_exit=on_conv_exit)


@dp.callback_query_handler(text=TextQueries.DEL_MESSAGE, state='*')
async def delete_msg(msg: types.Message):
    await msg.delete()
