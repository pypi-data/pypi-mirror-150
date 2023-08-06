from dataclasses import dataclass
import pandas as pd
from vptrade.plots.visualize import show_plot


@dataclass
class Oscillator:
    data: pd

    @show_plot("rsi")
    def rsi(self, period: int, volume: str, show: str = "single", save: str = "rsi_img.png") -> list:
        """
        Relative Strength Index
        :param period:
        :param volume:
        :param show:
        :param save:
        :return:
        """
        delta = self.data[volume].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=period, adjust=False).mean()
        ema_down = down.ewm(com=period, adjust=False).mean()
        rs = ema_up / ema_down
        self.data['RSI'] = 100 - (100 / (1 + rs))
        return self.data


