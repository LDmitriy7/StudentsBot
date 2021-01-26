"""Main script, starts bot in long-polling mode."""

from aiogram import executor

from loader import dp


async def on_startup(*args):
    import logging
    import handlers
    import middlewares

    logging.basicConfig(level=20)
    logger = logging.getLogger(__name__)
    logger.info('Import %s', middlewares)
    logger.info('Import %s', handlers)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
