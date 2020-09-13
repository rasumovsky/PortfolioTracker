import numpy as np
import matplotlib.pyplot as plt


def get_confidence_interval(values):
    num_simulations = len(values)
    # Find the median, 1, and 2 std dev values.
    probs = [0.045, 0.317, 0.5, 0.683, 0.955]
    indices = [int(prob * float(num_simulations)) for prob in probs]
    lower_2s = []
    lower_1s = []
    median = []
    upper_1s = []
    upper_2s = []
    for year in range(len(values[0])):
        yearly_values = [values[sim][year] for sim in range(num_simulations)]
        yearly_values.sort()
        lower_2s.append(yearly_values[indices[0]])
        lower_1s.append(yearly_values[indices[1]])
        median.append(yearly_values[indices[2]])
        upper_1s.append(yearly_values[indices[3]])
        upper_2s.append(yearly_values[indices[4]])
    return lower_2s, lower_1s, median, upper_1s, upper_2s


def get_crossing_dates(values, years, threshold):
    results = []
    for v in values:
        for y in range(len(years)-1):
            if ((v[y+1] > threshold and v[y] < threshold) or
                (v[y+1] < threshold and v[y] > threshold)):
                results.append(years[y])
                break
    return results


def plot_ci(x, ys, xlabel, ylabel, title, start_year, end_year):
    lower_2s, lower_1s, median, upper_1s, upper_2s = get_confidence_interval(ys)
    fig, ax = plt.subplots(figsize=(10,5))
    years = range(start_year, end_year + 1, 1)
    ax.plot(x, median, label='median income', color='r')
    ax.fill_between(years, lower_2s, upper_2s, facecolor='r', alpha=0.15, label='$\pm2\sigma$')
    ax.fill_between(years, lower_1s, upper_1s, facecolor='r', alpha=0.35, label='$\pm1\sigma$')
    ax.legend(loc=1)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.grid()
    plt.show()


def plot_two_ci(x, ys1, ys2, label1, label2, xlabel, ylabel, title, start_year, end_year,
                yrange=None, logy=False):
    lower_2s_1, lower_1s_1, median_1, upper_1s_1, upper_2s_1 = get_confidence_interval(ys1)
    lower_2s_2, lower_1s_2, median_2, upper_1s_2, upper_2s_2 = get_confidence_interval(ys2)
    fig, ax = plt.subplots(figsize=(10,5))
    years = range(start_year, end_year + 1, 1)
    ax.plot(x, median_1, label=label1, color='g')
    ax.fill_between(years, lower_2s_1, upper_2s_1, facecolor='g', alpha=0.15, label='$\pm2\sigma$')
    ax.fill_between(years, lower_1s_1, upper_1s_1, facecolor='g', alpha=0.35, label='$\pm1\sigma$')
    ax.plot(x, median_2, label=label2, color='b')
    ax.fill_between(years, lower_2s_2, upper_2s_2, facecolor='b', alpha=0.15, label='$\pm2\sigma$')
    ax.fill_between(years, lower_1s_2, upper_1s_2, facecolor='b', alpha=0.35, label='$\pm1\sigma$')
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    if yrange:
      ax.set_ylim(yrange)
    ax.legend(loc='best')
    ax.grid()
    if logy:
        plt.yscale('log')
    plt.show()
