from aiogram import types

import functions as funcs
from loader import dp


@dp.inline_handler(lambda query: query.query, state='*')
async def suggest_subjects(query: types.InlineQuery):
    fit_subjects = await funcs.find_subjects()
    await query.answer(results=fit_subjects)
