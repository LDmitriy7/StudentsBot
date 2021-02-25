from aiogram import types

import functions as funcs
from loader import dp


@dp.inline_handler(lambda iquery: iquery.query, state='*')
async def suggest_subjects(iquery: types.InlineQuery):
    fit_subjects = await funcs.find_subjects()
    await iquery.answer(results=fit_subjects)
