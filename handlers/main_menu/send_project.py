from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText
from aiogram.utils.exceptions import TelegramAPIError

import functions as funcs
from data_types import SendTo, Prefixes
from keyboards import inline_funcs
from keyboards.markup import Main, ConfirmProject
from loader import dp
from questions import CreateProjectConv as States


@dp.message_handler(text=ConfirmProject.SEND, state=States.confirm, sdata={'send_to': SendTo.CHANNEL})
async def send_project_to_channel():
    project = await funcs.save_project()
    post = await funcs.send_post(project.id, project.data)
    return UpdateData(), QuestText(f'<a href="{post.url}">Проект</a> успешно создан', Main())


@dp.message_handler(text=ConfirmProject.SEND, state=States.confirm, sdata={'send_to': SendTo.WORKER})
async def send_project_to_worker(msg: types.Message, user_name):
    project = await funcs.save_project()
    await msg.answer('Идет отправка...', reply_markup=Main())
    chats = await funcs.create_and_save_groups(project.client_id, project.worker_id, project.id)

    try:
        await funcs.send_chat_link_to_worker(user_name, project.worker_id, chats.worker_chat.link)
    except TelegramAPIError:
        text = 'Не могу отправить проект этому исполнителю'
    else:
        keyboard = inline_funcs.link_button('Перейти в чат', chats.client_chat.link)
        text = QuestText('Проект отправлен, ожидайте автора в чате', keyboard)
    return UpdateData(), text


@dp.message_handler(text=ConfirmProject.SEND, state=States.confirm, sdata={'send_to': None})
async def send_offer_keyboard(msg: types.Message):
    project = await funcs.save_project()
    await msg.answer('Проект успешно создан', reply_markup=Main())
    text = 'Теперь вы можете отправить проект <b>исполнителю</b>'
    keyboard = inline_funcs.offer_project(project.id)
    return UpdateData(), QuestText(text, keyboard)


@dp.inline_handler(cprefix=Prefixes.OFFER_PROJECT_)
async def send_offer_to_worker(iquery: types.InlineQuery, payload: str):
    article = funcs.make_offer_project_article(payload)
    await iquery.answer([article], cache_time=0, is_personal=True)
