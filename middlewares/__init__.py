from loader import dp
from middlewares.conv_manager import ConvManager
from middlewares.subscribe import CheckSubscription
from middlewares.my_profile import UpdatePage

dp.setup_middleware(ConvManager())
dp.setup_middleware(CheckSubscription())
dp.setup_middleware(UpdatePage())
