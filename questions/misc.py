from aiogram.contrib.questions import QuestText, ConvState, ConvStatesGroup

from keyboards.markup import Back

bid_text = QuestText('Отправьте текст для заявки', Back(BACK=None))


class SendBidConv(ConvStatesGroup):
    bid_text = ConvState(bid_text)
