from aiogram.contrib.questions import QuestText, ConvState, ConvStatesGroup

from keyboards import markup

bid_text = QuestText('Отправьте текст для заявки', markup.cancel_kb)


class SendBidConv(ConvStatesGroup):
    bid_text = ConvState(bid_text)
