from aiogram import types
from aiogram.contrib.questions import SingleConvStatesGroup, ConvState, ConvStatesGroup, QuestFunc

import keyboards as KB
from subfuncs.currents2 import Currents

ask_work_price = 'Введите цену в гривнах'


class ForGroups(SingleConvStatesGroup):
    ask_work_price = ConvState(ask_work_price)


@QuestFunc
@Currents.set
async def ask_quality(*, query_msg: types.Message):
    text = 'Оцените качество выполненной работы'
    keyboard = KB.Rates(row_width=5)
    await query_msg.edit_text(text, reply_markup=keyboard)


@QuestFunc
@Currents.set
async def ask_terms(*, query_msg: types.Message):
    text = 'Оцените сроки выполнения работы'
    keyboard = KB.Rates(row_width=5)
    await query_msg.edit_text(text, reply_markup=keyboard)


@QuestFunc
@Currents.set
async def ask_contact(*, query_msg: types.Message):
    text = 'Оцените контактность исполнителя'
    keyboard = KB.Rates(row_width=5)
    await query_msg.edit_text(text, reply_markup=keyboard)


@QuestFunc
@Currents.set
async def ask_text(*, query_msg: types.Message):
    text = 'Напишите небольшой отзыв'
    await query_msg.edit_text(text)


class FeedbackConv(ConvStatesGroup):
    ask_quality = ConvState(ask_quality)
    ask_terms = ConvState(ask_terms)
    ask_contact = ConvState(ask_contact)
    ask_text = ConvState(ask_text)
