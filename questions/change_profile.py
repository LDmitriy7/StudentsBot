from aiogram.contrib.questions import ConvState, ConvStatesGroup, QuestText

from keyboards import markup

nickname = QuestText('Придумайте себе никнейм', markup.cancel_kb)

phone_number = QuestText('Отправьте номер телефона', markup.phone_number)

email = QuestText('Отправьте email', markup.miss_kb)

biography = QuestText('Напишите о себе все, что считаете нужным', markup.go_back_kb)

works = QuestText(
    'Отправьте примеры ваших работ (только фото), отправляйте фото по одному!',
    markup.ready_kb,
)


#
# class ChangePhoneConv(ConvStatesGroup):
#     phone_number = ConvState(phone_number)
#
#
# class ChangeEmailConv(ConvStatesGroup):
#     email = ConvState(email)
#
#
# class ChangeBiography(ConvStatesGroup):
#     biography = ConvState(biography)
#
#
# class ChangeWorks(ConvStatesGroup):
#     works = ConvState(works)
#
#
# class ChangeNickname(ConvStatesGroup):
#     nickname = ConvState(nickname)

class ChangeProfile(ConvStatesGroup):
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
