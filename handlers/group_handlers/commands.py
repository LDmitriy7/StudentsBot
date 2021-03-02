from aiogram.contrib.questions import QuestText

import functions as funcs
from loader import dp


@dp.message_handler(commands='menu')
async def send_keyboard(chat_type):
    if chat_type == 'group':
        keyboard = await funcs.get_group_keyboard()
        return QuestText('Доступные команды:', keyboard)
    else:
        return 'Эта команда доступна только в группах'
