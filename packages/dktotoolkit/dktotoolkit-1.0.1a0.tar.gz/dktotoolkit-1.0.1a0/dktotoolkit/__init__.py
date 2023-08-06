"""
toolkit library, for Discord Catho bot ("dkto")
"""

from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)

from .dict import dict2obj
from .list import replace_with_mask
from .datestr import parser_date
from .envvar import load_dotenv, getEnvironVar, getTimesReminder

