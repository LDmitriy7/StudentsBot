from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import keyboards as KB
from loader import dp, users_db
from questions import ChangeProfile as States
from texts import templates
from texts.subjects import ALL_SUBJECTS


@dp.message_handler(button=KB.for_worker.MY_SUBJECTS)
async def send_my_subjects(user_id: int):
    account = await users_db.get_account_by_id(user_id)
    if account.subjects:
        text = templates.form_subjects_text(account.subjects)
    else:
        text = 'Вы еще не выбрали ни одного предмета'
    return QuestText(text, KB.subjects)


# --- Изменение предметов по спискам ---

@dp.callback_query_handler(button=KB.subjects.CHANGE_BY_LISTS)
async def start_change_subjects(user_id: int):
    account = await users_db.get_account_by_id(user_id)
    return UpdateData({'subjects': account.subjects}, new_state=States.subjects)


@dp.callback_query_handler(button=KB.subjects_categories.BUTTONS, state=States.subjects)
async def send_subjects_by_category(msg: types.Message, data: str, sdata: dict):
    user_subjects = sdata.get('subjects', [])
    keyboard = KB.SubjectsForCategory(data, 0, user_subjects)
    await msg.edit_text('Предметы категории:', reply_markup=keyboard)


@dp.callback_query_handler(button=KB.SubjectsForCategory.GO_BACK, state=States.subjects)
async def go_back_to_subjects_categories(msg: types.Message):
    await msg.edit_text('Категории предметов:', reply_markup=KB.subjects_categories)


@dp.callback_query_handler(button=[KB.SubjectsForCategory.TURN_PAGE_LEFT,
                                   KB.SubjectsForCategory.TURN_PAGE_RIGHT],
                           state=States.subjects)
async def get_new_subjects_page(msg: types.Message, suffix: str, sdata: dict):
    category, page = suffix.rsplit(':', maxsplit=1)
    user_subjects = sdata.get('subjects', [])
    keyboard = KB.SubjectsForCategory(category, int(page), user_subjects)
    await msg.edit_text('Предметы категории:', reply_markup=keyboard)


@dp.callback_query_handler(text=ALL_SUBJECTS, state=States.subjects)
async def change_subject(msg: types.Message, data: str, sdata: dict):
    keyboard = msg.reply_markup

    if data in sdata.get('subjects', []):
        update_data = UpdateData(remove_data={'subjects': data}, new_state=None)

        # remove check mark
        for row in keyboard.inline_keyboard:
            for button in row:
                if button.callback_data == data:
                    button.text = button.text.replace(' ✅', '')
                    break

    else:
        update_data = UpdateData(extend_data={'subjects': data}, new_state=None)

        # add check mark
        for row in keyboard.inline_keyboard:
            for button in row:
                if button.text == data:
                    button.text += ' ✅'
                    break

    await msg.edit_reply_markup(keyboard)
    return update_data


@dp.message_handler(text=KB.ready.START_OVER, state=States.subjects)
async def reset_subjects():
    text = 'Осторожно, вы сбросили все предметы, но можете сделать отмену'
    return UpdateData(delete_keys='subjects', new_state=None), text


@dp.message_handler(text=KB.ready.READY, state=States.subjects)
async def finish_change_subjects(user_id: int, sdata: dict):
    await users_db.update_account_subjects(user_id, sdata.get('subjects', []))
    return UpdateData(), QuestText('Предметы обновлены', KB.for_worker)


# --- Изменение предметов вручную ---

@dp.callback_query_handler(text=KB.subjects.CHANGE_MANUALLY)
async def start_change_subjects_manually(user_id: int):
    account = await users_db.get_account_by_id(user_id)
    return UpdateData({'subjects': account.subjects}, new_state=States.subjects_manually)


@dp.message_handler(text=KB.ready.START_OVER, state=States.subjects_manually)
async def reset_subjects():
    text = 'Осторожно, вы сбросили все предметы, но можете сделать отмену'
    return UpdateData(delete_keys='subjects', new_state=None), text


@dp.message_handler(text=KB.ready.READY, state=States.subjects_manually)
async def finish_change_subjects(user_id: int, sdata: dict):
    await users_db.update_account_subjects(user_id, sdata.get('subjects', []))
    return UpdateData(), QuestText('Предметы обновлены', KB.for_worker)


@dp.message_handler(state=States.subjects_manually)
async def change_subject(text: str, sdata: dict):
    if text in sdata['subjects']:
        return UpdateData(remove_data={'subjects': text}, new_state=None), 'Предмет удален'
    else:
        return UpdateData(extend_data={'subjects': text}, new_state=None), 'Предмет добавлен'
