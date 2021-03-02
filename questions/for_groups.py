from aiogram import types
from aiogram.contrib.questions import SingleConvStatesGroup, ConvState, ConvStatesGroup, QuestFunc
from aiogram.dispatcher.currents import CurrentObjects

import keyboards as KB

ask_work_price = 'Введите цену в гривнах'


class ForGroups(SingleConvStatesGroup):
    ask_work_price = ConvState(ask_work_price)


@QuestFunc
@CurrentObjects.decorate
async def ask_quality(*, msg: types.Message):
    text = 'Оцените качество выполненной работы'
    await msg.edit_text(text, reply_markup=KB.rates)


@QuestFunc
@CurrentObjects.decorate
async def ask_terms(*, msg: types.Message):
    text = 'Оцените сроки выполнения работы'
    await msg.edit_text(text, reply_markup=KB.rates)


@QuestFunc
@CurrentObjects.decorate
async def ask_contact(*, msg: types.Message):
    text = 'Оцените контактность исполнителя'
    await msg.edit_text(text, reply_markup=KB.rates)


@QuestFunc
@CurrentObjects.decorate
async def ask_text(*, msg: types.Message):
    text = 'Напишите небольшой отзыв'
    await msg.edit_text(text)


class FeedbackConv(ConvStatesGroup):
    ask_quality = ConvState(ask_quality)
    ask_terms = ConvState(ask_terms)
    ask_contact = ConvState(ask_contact)
    ask_text = ConvState(ask_text)
