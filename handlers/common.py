from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import markup


@dp.message_handler(text='Отменить', state='*')
@dp.message_handler(commands='cancel', state='*')
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('Отменено', reply_markup=markup.main_kb)
