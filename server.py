"""Main script, starts bot in long-polling mode."""
from aiogram import Dispatcher


async def on_startup(dp: Dispatcher):
    import logging

    import middlewares
    import handlers

    logging.basicConfig(level=20)

    dp.throttling_rate_limit = 3
    dp.no_throttle_error = True


if __name__ == '__main__':
    from aiogram import executor
    from loader import dp

    executor.start_polling(dp, on_startup=on_startup)

__all__ = ['handlers', 'middlewares']
