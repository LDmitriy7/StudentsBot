"""Main script, starts bot in long-polling mode."""

from aiogram import executor

from loader import dp


async def on_startup(*args):
    import handlers
    import middlewares
    import logging

    logging.basicConfig(level=20)
    # logger.add('journal.log', level=20, mode='w', format='{function} | {message}')
    # logger.debug('Import {}', middlewares)
    # logger.debug('Import {}', handlers)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
