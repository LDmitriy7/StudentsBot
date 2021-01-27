from loader import dp
from middlewares.conv_manager import ConvManager
from middlewares.subscribe import CheckSubscription

dp.setup_middleware(ConvManager())
dp.setup_middleware(CheckSubscription())
