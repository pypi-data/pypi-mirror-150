from dataclasses import dataclass, field
import pandas as pd
import warnings


@dataclass
class VPTradeBase:
    data: str = field(default=None)
    path: str = field(default=None)

    def __post_init__(self):
        if self.data is None and self.path is None:
            raise "Data or Path must be included"
        if self.data is None and self.path is None:
            warnings.warn("please insert data or path parameter")

    def read_data(self):
        if self.path is not None:
            self.data = pd.read_csv(self.path,
                                    index_col="Date",
                                    parse_dates=True)
        return self.data


if __name__ == "__main__":
    base = VPTradeBase(path=r'C:\Users\forst\Downloads\TSLA.csv')
    print(base.read_data())
