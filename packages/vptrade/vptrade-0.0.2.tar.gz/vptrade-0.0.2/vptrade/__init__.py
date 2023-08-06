from . import version
from vptrade.indicators.trends import Trend
from vptrade.indicators.oscillators import Oscillator
from vptrade.plots import visualize
from vptrade.strategies import moving_average
from vptrade.base import VPTradeBase

__version_info__ = version.VERSION
__version__ = version.VERSION_TEXT




__all__ = [
    "Trend",
    "Oscillator",
    "visualize",
    "moving_average",
    "VPTradeBase",
]
