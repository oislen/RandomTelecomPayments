
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def distribution_plot(data, bins='auto', title=None):
    """
    """
    # set plot size and style
    sns.set(rc={'figure.figsize':(7, 7), "lines.linewidth": 0.7})
    sns.set_style("white")
    dist_plot = sns.histplot(data=data, bins=bins)
    if title != None:
        dist_plot.set_title(label=title)
    plt.show()
    plt.close()


def lift_plot(col, target, data, order = 'default', cut = None):
    """
    Plot a bar chart of the target variable against a given predictor
    """
    # take deep cut of data for temporary storage
    tmp_data = data.copy()
    # calculate the avergae rate of taking out a loan
    mean_y_yes = tmp_data[target].mean()
    # if quantile cutting col
    if cut != None:
        tmp_data[col] = pd.cut(x = tmp_data[col], bins = cut)
    # determine plot order based on bin height
    if order == 'default':
        plot_order = tmp_data.groupby(col)[target].mean().sort_values(ascending=False).index.values
    else:
        plot_order = order
    # set figure size
    plt.figure(figsize=(8, 6))
    # create bar plot
    sns.barplot(data = tmp_data, x = col, y = target, estimator = np.mean, errorbar = None, color = 'royalblue', order = plot_order)
    # format plot title, ticks and labels
    plt.title(f'{col} vs {target}', size = 20)
    plt.yticks(size = 15)
    plt.xticks(rotation = 45, size = 15)
    plt.xlabel(col, size = 18)
    plt.ylabel(target, size = 18)
    # red line indicates average rate of taking out a loan
    plt.axhline(y=mean_y_yes, color = 'red', linestyle = '--', linewidth = 3)
    # show and close plot
    plt.show()
    plt.close()
    return 0