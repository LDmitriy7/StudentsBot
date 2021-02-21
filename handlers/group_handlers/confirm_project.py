from aiogram import types
from aiogram.contrib.questions import QuestText
from aiogram.utils.markdown import hbold as b

from data_types import ProjectStatuses, UserRoles, Prefixes
from filters import find_pair_chat, QueryPrefix
from keyboards import inline_funcs
from keyboards.inline_funcs import GroupMenuKeyboard
from loader import dp, users_db, bot


@dp.callback_query_handler(text=GroupMenuKeyboard.CONFIRM_PROJECT,
                           pstatus=ProjectStatuses.IN_PROGRESS,
                           user_role=UserRoles.CLIENT)
async def ask_confirm_project(query: types.CallbackQuery):
    chat = await users_db.get_chat_by_id(query.message.chat.id)
    text = 'Вы точно хотите подтвердить выполнение проекта?'
    keyboard = inline_funcs.total_confirm_project(chat.project_id)
    return QuestText(text, keyboard)


@dp.callback_query_handler(find_pair_chat,
                           QueryPrefix(Prefixes.CONFIRM_PROJECT_),
                           pstatus=ProjectStatuses.IN_PROGRESS,
                           user_role=UserRoles.CLIENT)
async def confirm_project(query: types.CallbackQuery, pchat_id: int, payload: str):
    project = await users_db.get_project_by_id(payload)

    # TODO: полноценное обновление проекта
    await users_db.update_project_status(payload, ProjectStatuses.COMPLETED)
    await users_db.incr_balance(project.worker_id, project.data.price)

    worker_text = b('Заказчик подтвердил выполнение проекта, деньги перечислены на ваш счет.')
    await bot.send_message(pchat_id, worker_text)
    return b('Теперь вы можете написать отзыв')
