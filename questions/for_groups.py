from aiogram import types
from aiogram.contrib.currents import SetCurrent
from aiogram.contrib.questions import SingleConvStatesGroup, ConvState, ConvStatesGroup, QuestFunc

import keyboards as KB

ask_work_price = 'Введите цену в гривнах'


class ForGroups(SingleConvStatesGroup):
    ask_work_price = ConvState(ask_work_price)


@QuestFunc
@SetCurrent.query
async def ask_quality(*, query: types.CallbackQuery):
    text = 'Оцените качество выполненной работы'
    keyboard = KB.Rates(row_width=5)
    await query.message.edit_text(text, reply_markup=keyboard)


@QuestFunc
@SetCurrent.query
async def ask_terms(*, query: types.CallbackQuery):
    text = 'Оцените сроки выполнения работы'
    keyboard = KB.Rates(row_width=5)
    await query.message.edit_text(text, reply_markup=keyboard)


@QuestFunc
@SetCurrent.query
async def ask_contact(*, query: types.CallbackQuery):
    text = 'Оцените контактность исполнителя'
    keyboard = KB.Rates(row_width=5)
    await query.message.edit_text(text, reply_markup=keyboard)


@QuestFunc
@SetCurrent.query
async def ask_text(*, query: types.CallbackQuery):
    text = 'Напишите небольшой отзыв'
    await query.message.edit_text(text)


class FeedbackConv(ConvStatesGroup):
    ask_quality = ConvState(ask_quality)
    ask_terms = ConvState(ask_terms)
    ask_contact = ConvState(ask_contact)
    ask_text = ConvState(ask_text)
