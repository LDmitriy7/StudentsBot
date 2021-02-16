"""Main script, starts bot in long-polling mode."""
from aiogram import executor

from loader import dp


# Logic Levels:
# > [handlers, middlewares, filters, questions]
# >> [functions, loader]
# >>> [subfuncs, utils, database]
# >>>> [texts, keyboards, data_types, config]

async def on_startup(*args):
    import logging
    import filters
    import middlewares
    import handlers

    logging.basicConfig(level=20)
    logger = logging.getLogger(__name__)
    logger.debug('Import %s', filters)
    logger.debug('Import %s', middlewares)
    logger.debug('Import %s', handlers)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
