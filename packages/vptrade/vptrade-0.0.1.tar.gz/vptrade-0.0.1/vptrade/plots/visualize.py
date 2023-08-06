import matplotlib.pyplot as plt


def indicators(data, name, args, kwargs):
    ax = None
    if name == "bollinger_band":
        print(kwargs)
        ax = data[['Close', 'Upper', 'Lower']].plot(title='Bollinger Bands ' + "(" + kwargs['volume'] + " " + str(kwargs['period']) + ")", color=['blue', 'orange', 'yellow'])
        ax.fill_between(data.index, data['Lower'], data['Upper'], facecolor='orange', alpha=0.1)

    elif name == 'sma':
        ax = data[[kwargs['volume'], "SMA" + str(kwargs['period'])]].plot(title='Simple Moving Average',
                                                                          label="SMA" + str(kwargs['period']),
                                                                          figsize=(16, 8))
    elif name == 'ema':
        ax = data[[kwargs['volume'], "EMA" + str(kwargs['period'])]].plot(title='Exponential Moving Average',
                                                                          label="EMA" + str(kwargs['period']),
                                                                          figsize=(16, 8))
    elif name == 'cma':
        ax = data[[kwargs['volume'], "CMA" + str(kwargs['period'])]].plot(title='Cumulative Moving Average',
                                                                          label="CMA" + str(kwargs['period']),
                                                                          figsize=(16, 8))
    elif name == 'smma':
        ax = data[[kwargs['volume'], "SMMA" + str(kwargs['period'])]].plot(title='Smoothed Moving Average',
                                                                           label="SMMA" + str(kwargs['period']),
                                                                           figsize=(16, 8))

    elif name == 'lwma':
        ax = data[[kwargs['volume'], "LWMA" + str(kwargs['period'])]].plot(title='Linear-Weighted Moving Average',
                                                                           label="LWMA" + str(kwargs['period']),
                                                                           figsize=(16, 8))

    elif name == 'rsi':
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.get_xaxis().set_visible(False)
        fig.suptitle('Relative Strength Index ' + "(" + kwargs['volume'] + " " + str(kwargs['period']) + ")")
        data[kwargs['volume']].plot(ax=ax1)
        ax1.set_ylabel('Price')
        data['RSI'].plot(ax=ax2)
        ax2.set_ylim(0, 100)
        ax2.axhline(30, color='r', linestyle='--')
        ax2.axhline(70, color='r', linestyle='--')
        ax2.set_ylabel('RSI')

    return ax


def show_plot(indicator):
    def wrapper(func):
        def inner(*args, **kwargs):
            value = func(*args, **kwargs)
            try:
                if 'show' in kwargs:
                    if kwargs['show']:
                        fig = indicators(value, indicator, args, kwargs)
                        plt.show()
                if 'save' in kwargs:
                    fig = indicators(value, indicator, args, kwargs)
                    fig.figure.savefig(kwargs['save'])
            except IndexError as e:
                print("Should be use kwargs instead of args")
                print(e)
            return value

        return inner

    return wrapper
