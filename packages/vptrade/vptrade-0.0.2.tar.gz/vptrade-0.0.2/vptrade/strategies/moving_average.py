from dataclasses import dataclass
import pandas as pd
import numpy as np
from vptrade.plots.visualize import show_plot


@dataclass
class MovingAverageStrategy:

    @classmethod
    def combine(cls, indicators: list):
        data = pd.DataFrame()
        data[indicators[0].iloc[:, [0]].columns] = indicators[0].iloc[:, [0]]  # get real price
        # get moving average price
        for i in indicators:
            data[i.iloc[:, [1]].columns] = i.iloc[:, [1]]
        return data

    @show_plot('ema')
    def crossover(self, indicators: list, show: str = "strategy", save: str = "ema_img.png") -> pd.DataFrame:
        """
        Crossover Moving Averages Strategy
        :param indicators: list = multiple MA indicators and must be ascending. ex: [ema_14,ema_100, ema_200,...]
        :param show: str = (Optional) Only 'strategy' available
        :param save: str = (Optional)
        :return: List = [ Date, Close        EMA20      EMA100      EMA200  Signal  Position]
        Position 0 mean nothing
        position -1 sell signal
        position 1 buy signal
        """
        data = self.combine(indicators)
        data['Signal'] = 0.0
        data['Signal'] = np.where(data['EMA20'] > data['EMA200'], 1.0, 0.0)
        data["Position"] = data["Signal"].diff()
        return data
