from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import inline_plain, markup
from loader import dp, users_db
from states import MiscStates as States
from texts import templates
from questions.misc import HandleException


@dp.message_handler(text='Мои предметы')
async def send_my_subjects(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    subjects = account.get('subjects', [])
    if subjects:
        text = templates.form_subjects_text(subjects)
    else:
        text = '<b>Вы еще не выбрали ни одного предмета</b>'
    keyboard = inline_plain.subjects
    await msg.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text=inline_plain.subjects.CHANGE_SUBJECTS)
async def start_change_subjects(query: types.CallbackQuery):
    msg = query.message
    account = await users_db.get_account_by_id(query.from_user.id)
    subjects = account.get('subjects', [])

    text1 = 'Введите название предмета'
    keyboard1 = markup.ready_kb
    text2 = 'Вы можете использовать поиск'
    keyboard2 = inline_plain.find_subject

    await States.change_subjects.set()
    await msg.answer(text1, reply_markup=keyboard1)
    await msg.answer(text2, reply_markup=keyboard2)
    return {'subjects': subjects}


@dp.message_handler(text='Начать заново', state=States.change_subjects)
async def reset_subjects(msg: types.Message):
    await msg.answer('Осторожно, вы сбросили все предметы, но можете сделать отмену')
    return {'subjects': ()}, HandleException


@dp.message_handler(text='Готово', state=States.change_subjects)
async def finish_change_subjects(msg: types.Message, state: FSMContext):
    udata = await state.get_data()
    subjects = udata['subjects']
    await users_db.update_account_subjects(msg.from_user.id, subjects)
    await msg.answer('Предметы обновлены', reply_markup=markup.worker_kb)


@dp.message_handler(state=States.change_subjects)
async def change_subject(msg: types.Message, state: FSMContext):
    subject = msg.text

    async with state.proxy() as udata:
        subjects: list = udata['subjects']
        if subject in subjects:
            subjects.remove(subject)
            text = 'Предмет удален'
        else:
            subjects.append(subject)
            text = 'Предмет добавлен'
    await msg.answer(text)
    return HandleException()
