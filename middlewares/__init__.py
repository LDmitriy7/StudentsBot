from aiogram.contrib.middlewares.logging import LoggingMiddleware

from loader import dp
from middlewares.main import *

dp.setup_middleware(LoggingMiddleware())
