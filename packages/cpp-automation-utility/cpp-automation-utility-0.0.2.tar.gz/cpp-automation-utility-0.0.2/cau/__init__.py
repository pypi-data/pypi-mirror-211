"""
CAU
"""
import functools

import colorlog

from .wrappers import *
from .timer import timer

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s"))
logger = colorlog.getLogger("CAU")
logger.addHandler(handler)
logger.setLevel(colorlog.INFO)
