import matplotlib.pyplot as plt

insert = None


def indicators(data, name, args, kwargs):
    ax = None
    periodName = name.upper() + str(kwargs['period'])
    listMA = {'sma': 'Simple Moving Average', 'ema': 'Exponential Moving Average',
              'cma': 'Cumulative Moving Average', 'smma': 'Smoothed Moving Average',
              'lwma': 'Linear-Weighted Moving Average'}

    if name == "bollinger_band":
        print(kwargs)
        ax = data[['Close', 'Upper', 'Lower']].plot(
            title='Bollinger Bands ' + "(" + kwargs['volume'] + " " + str(kwargs['period']) + ")",
            color=['blue', 'orange', 'yellow'])
        ax.fill_between(data.index, data['Lower'], data['Upper'], facecolor='orange', alpha=0.1)

    elif name.lower() in listMA:
        ax = data[[kwargs['volume'], periodName]].plot(title=listMA[name],
                                                       ax=insert,
                                                       label=periodName,
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
            global insert
            value = func(*args, **kwargs)
            try:
                if 'show' in kwargs:
                    if kwargs['show'] == "single":
                        fig = indicators(value, indicator, args, kwargs)
                        plt.show()
                    elif kwargs['show'] == "combine":
                        fig = indicators(value, indicator, args, kwargs)
                        insert = fig
                    elif kwargs['show'] == "strategy":
                        for column in value.columns[1:4]:
                            period = "".join([str(word) for word in column if word.isdigit()])
                            name = column.split(period)[0]
                            kwargs['period'] = period
                            kwargs['volume'] = value.columns[0]
                            fig = indicators(value, name.lower(), args, kwargs)
                            insert = fig
                        markprice(value)

                if 'save' in kwargs:
                    fig = indicators(value, indicator, args, kwargs)
                    fig.figure.savefig(kwargs['save'])
            except IndexError as e:
                print("Should be use kwargs instead of args")
                print(e)
            return value

        return inner

    return wrapper


def show_multiple_plot(data, indicator, info):
    pass


def markprice(data):
    plt.plot(data[data['Position'] == 1].index,
             data.iloc[:, [1]][data['Position'] == 1],
             '^', markersize=15, color='g', alpha=0.7, label='buy')

    # plot 'sell' signals
    plt.plot(data[data['Position'] == -1].index,
             data.iloc[:, [1]][data['Position'] == -1],
             'v', markersize=15, color='r', alpha=0.7, label='sell')
    plt.ylabel('Price', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.title('CrossOver', fontsize=20)
    plt.legend()
    plt.grid()
    plt.show()


def show():
    plt.show()
