"""Main script, starts bot in long-polling mode."""
from aiogram import executor

from loader import dp


# Logic Levels:
# [handlers, middlewares] > functions > utils > [texts, keyboards, datatypes]

async def on_startup(*args):
    import logging
    import handlers
    import middlewares
    import filters

    logging.basicConfig(level=20)
    logger = logging.getLogger(__name__)
    logger.debug('Import %s', handlers)
    logger.debug('Import %s', middlewares)
    logger.debug('Import %s', filters)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
