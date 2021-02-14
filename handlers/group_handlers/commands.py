from aiogram import types

import functions as funcs
from loader import dp


@dp.message_handler(commands='menu')
async def send_keyboard(msg: types.Message):
    if msg.chat.type == 'group':
        keyboard = await funcs.get_group_keyboard(msg.chat)
        await msg.answer('Доступные команды:', reply_markup=keyboard)
    else:
        await msg.answer('Эта команда доступна только в группах')
