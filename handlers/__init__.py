"""Imports all handlers sets.
1) common (special) handlers must be at the top
2) balance should be closer to the top (for guaranteed deposits)
3) errors must be at the end.
"""

from handlers import common
from handlers import inline
from handlers import bids
from handlers import registration

from handlers import main_menu
from handlers import worker_menu

from handlers import projects

from handlers import errors
