from loader import dp, users_db
from aiogram import types
from questions import registration as questions
from keyboards.inline_text import MyProfileKeyboard
from keyboards import inline_text, markup
from states import ChangeProfile as States
from functions import registration as funcs
from functions import common as cfuncs
from questions.misc import HandleException
from aiogram.dispatcher import FSMContext


@dp.message_handler(text='Мой профиль')
async def send_profile(msg: types.Message):
    await msg.answer('Ваш профиль: здесь будут данные...', reply_markup=inline_text.change_profile)


@dp.callback_query_handler(text=MyProfileKeyboard.CHANGE_BUTTONS)
async def start_change_profile(query: types.CallbackQuery):
    states_dict = {
        'Изменить никнейм': (States.nickname, questions.nickname),
        'Изменить номер телефона': (States.phone_number, questions.phone_number),
        'Изменить email': (States.email, questions.email),
        'Изменить биографию': (States.biography, questions.biography),
        'Изменить примеры работ': (States.works, questions.works),
    }
    new_state, new_quest = states_dict[query.data]

    await new_state.set()
    await query.message.answer(new_quest.text, reply_markup=new_quest.keyboard)

    if new_state == States.works:
        account = await users_db.get_account_by_id(query.from_user.id)
        works = account['profile'].get('works', [])
        return {'works': works}


@dp.message_handler(state=States.nickname)
async def process_nickname(msg: types.Message, state: FSMContext):
    username = msg.from_user.username
    all_nicknames = await funcs.get_all_nicknames()

    if msg.text == username:
        return HandleException('Пожалуйста, не используйте свой юзернейм')
    elif msg.text in all_nicknames:
        return HandleException('Этот никнейм уже занят')

    await users_db.update_account(msg.from_user.id, {'profile.nickname': msg.text})
    await msg.answer('Никнейм обновлен', reply_markup=markup.worker_kb)
    await state.finish()


@dp.message_handler(text='Пропустить', state=States.phone_number)
async def miss_phone_number(msg: types.Message, state: FSMContext):
    await users_db.update_account(msg.from_user.id, {'profile.phone_number': None})
    await msg.answer('Номер телефона сброшен', reply_markup=markup.worker_kb)
    await state.finish()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=States.phone_number)
async def process_phone_number(msg: types.Message, state: FSMContext):
    phone_number = msg.contact.phone_number
    await users_db.update_account(msg.from_user.id, {'profile.phone_number': phone_number})
    await msg.answer('Номер телефона обновлен', reply_markup=markup.worker_kb)
    await state.finish()


@dp.message_handler(state=States.email)
async def process_email(msg: types.Message, state: FSMContext):
    if msg.text == 'Пропустить':
        email = None
        text = 'Email сброшен'
    elif '@' in msg.text:
        email = msg.text
        text = 'Email обновлен'
    else:
        return HandleException('Похоже, вы ошиблись')
    await users_db.update_account(msg.from_user.id, {'profile.email': email})
    await msg.answer(text, reply_markup=markup.worker_kb)
    await state.finish()


@dp.message_handler(state=States.biography)
async def process_biography(msg: types.Message, state: FSMContext):
    if msg.text == 'Пропустить':
        biography = None
        text = 'Биография сброшена'
    elif 15 < len(msg.text):
        biography = msg.text
        text = 'Биография обновлена'
    else:
        return HandleException('Напишите не меньше 15 символов')
    await users_db.update_account(msg.from_user.id, {'profile.biography': biography})
    await msg.answer(text, reply_markup=markup.worker_kb)
    await state.finish()


@dp.message_handler(content_types=['photo'], state=States.works)
async def process_works(msg: types.Message):
    photo_id = cfuncs.get_file_obj(msg)[1]
    return {'works': [photo_id]}


@dp.message_handler(text=['Готово', 'Сбросить выбор'], state=States.works)
async def process_works_finish(msg: types.Message, state: FSMContext):
    if msg.text == 'Сбросить выбор':
        return {'works': ()}, HandleException('Осторожно, вы сбросили все работы')

    udata = await state.get_data()
    works = udata.get('works', [])
    await users_db.update_account(msg.from_user.id, {'profile.works': works})
    await msg.answer('Примеры работ обновлены', reply_markup=markup.worker_kb)
    await state.finish()
