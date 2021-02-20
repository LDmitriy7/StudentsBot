from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.questions import QuestText
from aiogram.contrib.middlewares.conversation import UpdateData

from keyboards import inline_plain, markup
from loader import dp, users_db
from questions import ChangeProfile as States
from texts import templates


@dp.message_handler(text='Мои предметы')
async def send_my_subjects(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    if account.subjects:
        text = templates.form_subjects_text(account.subjects)
    else:
        text = '<b>Вы еще не выбрали ни одного предмета</b>'
    return QuestText(text, inline_plain.subjects)


@dp.callback_query_handler(text=inline_plain.subjects.CHANGE_SUBJECTS)
async def start_change_subjects(query: types.CallbackQuery):
    account = await users_db.get_account_by_id(query.from_user.id)
    return UpdateData({'subjects': account.subjects}, new_state=States.subjects)


@dp.message_handler(text='Начать заново', state=States.subjects)
async def reset_subjects(msg: types.Message):
    text = 'Осторожно, вы сбросили все предметы, но можете сделать отмену'
    return UpdateData(delete_keys='subjects', new_state=None), text


@dp.message_handler(text='Готово', state=States.subjects)
async def finish_change_subjects(msg: types.Message, state: FSMContext):
    udata = await state.get_data()
    await users_db.update_account_subjects(msg.from_user.id, udata.get('subjects', []))
    return UpdateData(on_conv_exit=QuestText('Предметы обновлены', markup.worker_kb))


@dp.message_handler(state=States.subjects)
async def change_subject(msg: types.Message, state: FSMContext):
    udata = await state.get_data()
    if msg.text in udata['subjects']:
        return UpdateData(remove_data={'subjects': msg.text}, new_state=None), 'Предмет удален'
    else:
        return UpdateData(extend_data={'subjects': msg.text}, new_state=None), 'Предмет добавлен'
