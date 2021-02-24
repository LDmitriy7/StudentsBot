from aiogram import Dispatcher
from aiogram.dispatcher.filters import BoundFilter


class StorageData(BoundFilter):
    """Check if filter is subdict of storage values [current User+Chat]."""

    key = 'udata'

    def __init__(self, udata: dict):
        self.filter = udata

    async def check(self, *args) -> bool:
        state_ctx = Dispatcher.get_current().current_state()
        udata = await state_ctx.get_data()
        for key, value in self.filter.items():

            try:
                if udata[key] != value:
                    return False
            except KeyError:
                return False

        return True
