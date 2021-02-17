from loader import dp
from middlewares.my_profile import UpdatePage
from middlewares.subscribe import CheckSubscription
from middlewares.test import UserDataUpdater, SwitchConvState, AskQuestion


def setup(middlewares: list):
    for m in middlewares:
        dp.setup_middleware(m())


setup([UserDataUpdater, SwitchConvState, AskQuestion, CheckSubscription, UpdatePage])
