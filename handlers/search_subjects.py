from aiogram import types

import functions as funcs
from loader import dp


@dp.inline_handler(lambda query: query.query, state='*')
async def suggest_subjects(query: types.InlineQuery):
    await query.answer(results=funcs.find_subjects())
