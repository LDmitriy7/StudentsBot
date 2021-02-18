from aiogram import types
from aiogram.dispatcher import FSMContext

import functions as funcs
from data_types import data_classes, SendTo, ProjectStatuses
from keyboards import markup, inline_funcs
from loader import dp, users_db
from questions import CreateProjectConv as States


@dp.message_handler(text='Отправить проект', state=States.confirm)
async def send_project(msg: types.Message, state: FSMContext):
    udata = await state.get_data()
    client_id = msg.from_user.id
    worker_id = udata.get('worker_id')
    status = ProjectStatuses.ACTIVE
    send_to = udata.get('send_to')

    project_data = data_classes.ProjectData.from_dict(udata)
    project = data_classes.Project(project_data, status, client_id, worker_id)
    project_id = await users_db.add_project(project)

    if send_to == SendTo.CHANNEL:
        post_url = await funcs.send_post(project_id, status, project_data)
        await users_db.update_project_post_url(project_id, post_url)
        text = f'<a href="{post_url}">Проект</a> успешно создан'
        await msg.answer(text, reply_markup=markup.main_kb)

    elif send_to == SendTo.WORKER:
        await msg.answer('Идет отправка...', reply_markup=markup.main_kb)
        chats = await funcs.create_and_save_groups(client_id, worker_id, project_id)
        try:
            await funcs.send_chat_link_to_worker(msg.from_user.full_name, worker_id, chats.worker_chat.link)
        except:
            await msg.answer('Не могу отправить проект этому исполнителю')
        else:
            keyboard = inline_funcs.link_button('Перейти в чат', chats.client_chat.link)
            await msg.answer('Проект отправлен, ожидайте автора в чате', reply_markup=keyboard)

    elif send_to is None:
        await msg.answer('Проект успешно создан', reply_markup=markup.main_kb)
        text = 'Теперь вы можете отправить проект <b>исполнителю</b>'
        keyboard = inline_funcs.offer_project(project_id)
        await msg.answer(text, reply_markup=keyboard)
