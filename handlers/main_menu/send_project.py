from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError

import functions as funcs
from data_types import SendTo, Prefixes
from filters import InlinePrefix
from keyboards import markup, inline_funcs
from loader import dp
from questions import CreateProjectConv as States


@dp.message_handler(text='Отправить проект', state=States.confirm, udata={'send_to': SendTo.CHANNEL})
async def send_project_to_channel(msg: types.Message):
    project = await funcs.save_project()
    post_url = await funcs.send_post(project.id, project.data)
    text = f'<a href="{post_url}">Проект</a> успешно создан'
    await msg.answer(text, reply_markup=markup.main_kb)


@dp.message_handler(text='Отправить проект', state=States.confirm, udata={'send_to': SendTo.WORKER})
async def send_project_to_worker(msg: types.Message):
    project = await funcs.save_project()
    await msg.answer('Идет отправка...', reply_markup=markup.main_kb)
    chats = await funcs.create_and_save_groups(project.client_id, project.worker_id, project.id)

    try:
        await funcs.send_chat_link_to_worker(msg.from_user.full_name, project.worker_id, chats.worker_chat.link)
    except TelegramAPIError:
        await msg.answer('Не могу отправить проект этому исполнителю')
    else:
        keyboard = inline_funcs.link_button('Перейти в чат', chats.client_chat.link)
        await msg.answer('Проект отправлен, ожидайте автора в чате', reply_markup=keyboard)


@dp.message_handler(text='Отправить проект', state=States.confirm, udata={'send_to': None})
async def send_offer_keyboard(msg: types.Message):
    project = await funcs.save_project()
    await msg.answer('Проект успешно создан', reply_markup=markup.main_kb)
    text = 'Теперь вы можете отправить проект <b>исполнителю</b>'
    keyboard = inline_funcs.offer_project(project.id)
    await msg.answer(text, reply_markup=keyboard)


@dp.inline_handler(InlinePrefix(Prefixes.OFFER_PROJECT_))
async def send_offer_to_worker(query: types.InlineQuery, payload: str):
    article = funcs.make_offer_project_article(payload)
    await query.answer([article], cache_time=0, is_personal=True)
