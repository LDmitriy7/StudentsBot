"""Все для диалога: создание поста в канале."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import DeepLinkPrefix
from functions import common as cfuncs
from functions import projects, bids
from keyboards import inline_funcs, inline_plain, markup
from keyboards.inline_funcs import Prefixes
from keyboards.inline_plain import WorkTypeKeyboard
from loader import calendar, dp, users_db
from questions.misc import HandleException
from questions.personal_project import PersonalProjectConv as States
from questions.registration import RegistrationConv
from texts import main as texts
from type_classes import Bid


# вход в создание проекта +

@dp.message_handler(text='Личный проект 🤝')
async def ask_user_role(msg: types.Message):
    await msg.answer(texts.start_personal_project, reply_markup=markup.personal_project)


@dp.message_handler(text='Я исполнитель')
async def send_invite_project_keyboard(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    profile = account.get('profile') if account else None
    if profile:
        text = 'Выберите <b>заказчика</b> из списка своих чатов'
        keyboard = inline_plain.invite_project
        await msg.answer(text, reply_markup=keyboard)
    else:
        await msg.answer('Сначала пройдите регистрацию')
        return RegistrationConv


@dp.message_handler(text='Я заказчик')
async def entry_create_post(msg: types.Message):
    await msg.answer('Сначала заполните проект')
    return States  # входим в диалог


@dp.message_handler(DeepLinkPrefix(Prefixes.INVITE_PROJECT_))
async def entry_create_post_with_worker(msg: types.Message, payload: str):
    worker_id = int(payload)
    if msg.from_user.id == worker_id:
        return HandleException('<b>Вы сами не можете заполнить проект</b>')
    return States, {'worker_id': worker_id}  # входим в диалог с заданнным исполнителем


# заполнение проекта +

@dp.callback_query_handler(text=WorkTypeKeyboard.WORK_TYPE_BTNS, state=States.work_type)
async def process_work_type(query: types.CallbackQuery):
    return {'work_type': query.data}


@dp.message_handler(state=States.subject)
async def process_subject(msg: types.Message):
    return {'subject': msg.text}


@dp.callback_query_handler(calendar.filter(), state=States.date)
async def process_date(query: types.CallbackQuery, callback_data: dict):
    result = await cfuncs.handle_calendar_callback(query, callback_data)

    if isinstance(result, HandleException):
        return result  # распространяем исключение

    await query.answer(f'Выбрано: {result}')
    return {'date': str(result)}


@dp.message_handler(state=States.description)
async def process_description(msg: types.Message):
    min_len, max_len = 15, 500
    description = msg.text
    if min_len < len(description) < max_len:
        return {'description': description}
    return HandleException(f'Ошибка, описание должно быть от {min_len} до {max_len} символов')


@dp.message_handler(state=States.price)
async def process_price(msg: types.Message):
    if msg.text == 'Пропустить':
        price = None
    elif msg.text.isdigit():
        price = int(msg.text)
    else:
        return HandleException('Ошибка, введите только число')
    return {'price': price}


@dp.message_handler(state=States.note)
async def process_note(msg: types.Message):
    note = None if msg.text == 'Пропустить' else msg.text
    return {'note': note}


@dp.message_handler(content_types=['photo', 'document'], state=States.files)
async def process_file(msg: types.Message):
    file_obj = cfuncs.get_file_obj(msg)
    return {'files': [file_obj]}, HandleException()


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.files)
async def process_file_finish(msg: types.Message):
    if msg.text == 'Начать заново':
        return {'files': ()}, HandleException('Теперь выбирайте заново')
    return {'files': []}


# отправка проекта +

@dp.message_handler(text='Отправить проект', state=States.confirm)
async def send_personal_post(msg: types.Message, state: FSMContext):
    udata = await state.get_data()
    client_id = msg.from_user.id
    worker_id = udata.pop('worker_id', None)
    project_id = await projects.save_project(udata, client_id, worker_id)

    await msg.answer('Проект создан', reply_markup=markup.main_kb)

    if worker_id:
        bid = Bid(client_id, project_id, worker_id)
        bid_id = await users_db.add_bid(bid)
        await bids.send_client_bid(msg.from_user.full_name, bid.worker_id, bid_id)
        await msg.answer('Я позову вас в чат, когда исполнитель откликнется')
        return

    text = 'Теперь вы можете отправить проект <b>исполнителю</b>'
    keyboard = inline_funcs.offer_project(project_id)
    await msg.answer(text, reply_markup=keyboard)
