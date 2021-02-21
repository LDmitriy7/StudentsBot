from aiogram.contrib.questions import QuestText, ConvState, ConvStatesGroup

from keyboards.markup import BackKeyboard

bid_text = QuestText('Отправьте текст для заявки', BackKeyboard(BACK=None))


class SendBidConv(ConvStatesGroup):
    bid_text = ConvState(bid_text)
