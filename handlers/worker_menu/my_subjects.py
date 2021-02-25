from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import keyboards as KB
from loader import dp, users_db
from questions import ChangeProfile as States
from texts import templates


@dp.message_handler(text=KB.ForWorker.MY_SUBJECTS)
async def send_my_subjects(user_id: int):
    account = await users_db.get_account_by_id(user_id)
    if account.subjects:
        text = templates.form_subjects_text(account.subjects)
    else:
        text = '<b>Вы еще не выбрали ни одного предмета</b>'
    return QuestText(text, KB.Subjects())


@dp.callback_query_handler(text=KB.Subjects.CHANGE_SUBJECTS)
async def start_change_subjects(user_id: int):
    account = await users_db.get_account_by_id(user_id)
    return UpdateData({'subjects': account.subjects}, new_state=States.subjects)


@dp.message_handler(text=KB.Ready.START_OVER, state=States.subjects)
async def reset_subjects():
    text = 'Осторожно, вы сбросили все предметы, но можете сделать отмену'
    return UpdateData(delete_keys='subjects', new_state=None), text


@dp.message_handler(text=KB.Ready.READY, state=States.subjects)
async def finish_change_subjects(user_id: int, sdata: dict):
    await users_db.update_account_subjects(user_id, sdata.get('subjects', []))
    return UpdateData(), QuestText('Предметы обновлены', KB.ForWorker())


@dp.message_handler(state=States.subjects)
async def change_subject(text: str, sdata: dict):
    if text in sdata['subjects']:
        return UpdateData(remove_data={'subjects': text}, new_state=None), 'Предмет удален'
    else:
        return UpdateData(extend_data={'subjects': text}, new_state=None), 'Предмет добавлен'
