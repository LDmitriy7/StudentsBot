from aiogram.contrib.middlewares.logging import LoggingMiddleware

from loader import dp
from middlewares.main import ConvManager

dp.setup_middleware(LoggingMiddleware())
dp.setup_middleware(ConvManager())
