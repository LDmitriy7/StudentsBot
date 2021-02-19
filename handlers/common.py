"""Handle commands "Отменить", "Назад" and query for deleting bound message."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import texts
from data_types import TextQueries
from keyboards import markup
from loader import dp


@dp.message_handler(text='/start', state='*', chat_type='private')
async def send_welcome(msg: types.Message):
    quest = QuestText(texts.welcome, markup.main_kb)
    return UpdateData(new_state='exit', on_conv_exit=quest)


@dp.message_handler(text='Отменить', state='*')
@dp.message_handler(commands='cancel', state='*')
async def cancel(msg: types.Message):
    keyboard = markup.main_kb if msg.chat.type == 'private' else None
    quest = QuestText('Отменено', keyboard)
    return UpdateData(new_state='exit', on_conv_exit=quest)


@dp.message_handler(text='Назад', state='*')
async def go_back(msg: types.Message):
    on_conv_exit = QuestText('Отменено', markup.main_kb)
    return UpdateData(new_state='previous', on_conv_exit=on_conv_exit)


@dp.callback_query_handler(text=TextQueries.DEL_MESSAGE)
async def delete_msg(query: types.CallbackQuery):
    await query.message.delete()
