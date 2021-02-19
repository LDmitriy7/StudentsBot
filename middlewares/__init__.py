from aiogram.contrib.middlewares.conversation import UpdateUserState, AnswerOnReturn
from aiogram.contrib.middlewares.membership import CheckMembership

from config import CHANNEL_USERNAME
from loader import dp
from middlewares.my_profile import UpdatePage


def setup(middlewares: list):
    for m in middlewares:
        dp.setup_middleware(m())


dp.setup_middleware(CheckMembership(CHANNEL_USERNAME, f'Сначала подпишитесь на канал {CHANNEL_USERNAME}'))
setup([AnswerOnReturn, UpdateUserState])
