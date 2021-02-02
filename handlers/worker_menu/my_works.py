from loader import dp, users_db
from aiogram import types
from functions import common as cfuncs
from functions import my_works as funcs


@dp.message_handler(text='Мои работы')
async def send_works(msg: types.Message):
    projects = await users_db.get_projects_by_user(worker_id=msg.from_user.id)
    if projects:
        await msg.answer('<b>Список работ:</b>')
        await cfuncs.send_projects(msg, projects, with_note=False)
    else:
        await msg.answer('<b>У вас нет ни одной работы</b>')

# @dp.message_handler(text='Мои заявки')
# async def send_my_bids(msg: types.Message):
#     bids = await users_db.get_bids_by_user(worker_id=msg.from_user.id)
#     if bids:
#         await msg.answer('<b>Ваши заявки на проекты:</b>')
#         await funcs.send_bids(msg, bids)
#     else:
#         await msg.answer('<b>Вы не оставили ни одной заявки</b>')
