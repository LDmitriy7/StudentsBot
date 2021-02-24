from aiogram import types
from aiogram.contrib.questions import QuestText
from aiogram.utils.markdown import hbold as b

import functions as funcs
import keyboards as KB
from data_types import ProjectStatuses, UserRoles, Prefixes
from filters import find_pair_chat
from loader import dp, users_db, bot


@dp.callback_query_handler(text=KB.GroupMenu.CONFIRM_PROJECT,
                           pstatus=ProjectStatuses.IN_PROGRESS,
                           user_role=UserRoles.CLIENT)
async def ask_confirm_project(query: types.CallbackQuery):
    chat = await users_db.get_chat_by_id(query.message.chat.id)
    text = 'Вы точно хотите подтвердить выполнение проекта?'
    keyboard = KB.total_confirm_project(chat.project_id)
    return QuestText(text, keyboard)


@dp.callback_query_handler(find_pair_chat,
                           prefix=Prefixes.CONFIRM_PROJECT_,
                           pstatus=ProjectStatuses.IN_PROGRESS,
                           user_role=UserRoles.CLIENT)
async def confirm_project(query: types.CallbackQuery, pchat_id: int, payload: str):
    project = await users_db.get_project_by_id(payload)
    project.status = ProjectStatuses.COMPLETED

    await users_db.update_project_status(payload, project.status)
    await funcs.update_post(project.id, project.status, project.post_url, project.data)
    await users_db.incr_balance(project.worker_id, project.data.price)

    worker_text = b('Заказчик подтвердил выполнение проекта, деньги перечислены на ваш счет.')
    await bot.send_message(pchat_id, worker_text)
    return b('Теперь вы можете написать отзыв')
