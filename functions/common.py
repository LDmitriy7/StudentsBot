from datetime import date
from typing import List, Tuple, Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import MAIN_CHANNEL
from keyboards import inline_func, markup
from loader import bot, calendar, users_db
from questions import ALL_CONV_STATES, ConvStatesGroup
from questions.misc import ConvState, HandleException, ask_question
from texts import templates
from utils.inline_calendar import NotInitedException


async def get_balance(msg: types.Message) -> int:
    account = await users_db.get_account_by_id(msg.from_user.id)
    balance = account.get('balance', 0) if account else 0
    return balance


def get_file_obj(msg: types.Message) -> Tuple[str, str]:
    """Return Tuple[file_type, file_id]."""
    if msg.content_type == 'photo':
        file_id = msg.photo[-1].file_id
    elif msg.content_type == 'document':
        file_id = msg.document.file_id
    else:
        raise TypeError('Forbidden file type')

    return msg.content_type, file_id


async def handle_calendar_callback(query: types.CallbackQuery, callback_data) -> Union[date, HandleException]:
    try:
        date = calendar.handle_callback(query.from_user.id, callback_data)
    except NotInitedException:
        await query.answer('Попробуйте еще раз')
        return HandleException(_reinit_calendar)

    if date is None:
        return HandleException(_turn_calendar)
    return date


async def _reinit_calendar(msg: types.Message):
    keyboard = inline_func.make_calendar()
    await msg.edit_reply_markup(keyboard)


async def _turn_calendar(msg: types.Message):
    keyboard = calendar.get_keyboard()
    await msg.edit_reply_markup(keyboard)


async def send_file(chat_id: int, file_type: str, file_id: str):
    if file_type == 'photo':
        await bot.send_photo(chat_id, file_id)
    elif file_type == 'document':
        await bot.send_document(chat_id, file_id)


async def delete_post(post_url: str = None):
    """Удаляет пост из канала, если передана ссылка."""
    if post_url:
        post_id = post_url.split('/')[-1]
        await bot.delete_message(MAIN_CHANNEL, post_id)


async def send_projects(msg: types.Message, projects: List[dict], with_note=True, pick_button=False, del_button=False):
    """Отправляет в ответ проекты по списку."""
    for p in projects:
        post_data = p['data']
        status = p['status']
        project_id = str(p['_id'])

        text = templates.form_post_text(status, post_data, with_note)
        has_files = bool(post_data.get('files'))

        if del_button:
            is_active = p.get('status') == 'Активен'
        else:
            is_active = False

        keyboard = await inline_func.for_project(
            project_id,
            pick_btn=pick_button,
            del_btn=is_active,
            files_btn=has_files,
        )
        await msg.answer(text, reply_markup=keyboard)


async def ask_previous(msg: types.Message, state: FSMContext, states_group: ConvStatesGroup):
    new_state_name = await states_group.previous()

    if new_state_name is None:  # user has left conversation
        await state.finish()
        await msg.answer('Отменено', reply_markup=markup.main_kb)
    else:
        new_state: ConvState = ALL_CONV_STATES[new_state_name]
        await ask_question(msg, new_state.question)
