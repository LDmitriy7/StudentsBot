from aiogram.contrib.questions import QuestText, ConvState, ConvStatesGroup

import keyboards as KB

bid_text = QuestText('Отправьте текст для заявки', KB.Back)


class SendBidConv(ConvStatesGroup):
    bid_text = ConvState(bid_text)
