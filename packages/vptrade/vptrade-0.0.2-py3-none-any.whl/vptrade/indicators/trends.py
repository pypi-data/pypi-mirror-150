from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from vptrade.plots.visualize import show_plot
from vptrade.base import VPTradeBase


@dataclass
class Trend(VPTradeBase):
    """
    Trend Indicator
    - Moving Average (sma, ema, cma, smma, lwma)
    - Bollinger band
    """
    data: pd = field(default=None)
    path: str = field(default=None)

    def __post_init__(self):
        if self.path is not None:
            VPTradeBase(path=self.path)
            self.read_data()

    @show_plot('sma')
    def sma(self, period: int, volume: str, show: str = "single", save: str = "sma_img.png") -> list:
        """
        Simple Moving Average
        :param save:
        :param show:
        :param period:
        :param volume:
        :return:
        """
        data = self.data[volume].to_frame()
        data['SMA' + str(period)] = data[volume].rolling(period).mean()
        data.dropna(inplace=True)
        return data

    @show_plot('ema')
    def ema(self, period: int, volume: str, show: str = "single", save: str = "ema_img.png") -> list:
        """
        Exponential Moving Average
        :param show:
        :param save:
        :param period:
        :param volume:
        :return:
        """
        data = self.data[volume].to_frame()
        data['EMA' + str(period)] = data[volume].ewm(span=period).mean()
        data.dropna(inplace=True)
        return data

    @show_plot('cma')
    def cma(self, period: int, volume: str, show: str = "single", save: str = "cma_img.png") -> list:
        """
        Cumulative Moving Average
        :param period:
        :param show:
        :param save:
        :param volume:
        :return:
        """
        data = self.data[volume].to_frame()
        data['CMA' + str(period)] = data[volume].expanding().mean()
        return data

    @show_plot("smma")
    def smma(self, period: int, volume: str, show: str = "single", save: str = "cma_img.png") -> list:
        """
        Smoothed Moving Average
        :param show:
        :param save:
        :param period:
        :param volume:
        :return:
        """
        ema = self.ema(period, volume, show=show)
        smoothed = (ema * 2) - 1
        smoothed.rename(columns={"EMA30": 'SMMA' + str(period)}, inplace=True)
        return smoothed

    @show_plot("lwma")
    def lwma(self, period: int, volume: str, show: str = "single", save: str = "cma_img.png"):
        """
        Linear-Weighted Moving Average
        :param save:
        :param show:
        :param Data:
        :param period:
        :return:
        """
        weighted = np.arange(1, period + 1)
        self.data['LWMA' + str(period)] = self.data[volume].rolling(period).apply(lambda x: np.dot(x, weighted) /
                                                                                            weighted.sum(),
                                                                                  raw=True).to_list()
        self.data.dropna(inplace=True)
        return self.data

    @show_plot("bollinger_band")
    def bollinger_bands(self, period: int, volume: str, show: str = "single", save: str = "bolband_img.png") -> list:
        """
        Bollinger Bands
        :param period:
        :param volume:
        :param show:
        :param save:
        :return:
        """
        self.data['TP'] = (self.data['Close'] + self.data['Low'] + self.data['High']) / 3
        sma = self.sma(period=period, volume=volume)
        std = self.data[volume].rolling(period).std()
        upper_band = sma['SMA' + str(period)] + 2 * std
        lower_band = sma['SMA' + str(period)] - 2 * std
        self.data['Upper'] = upper_band.dropna()
        self.data['Lower'] = lower_band.dropna()

        return self.data
