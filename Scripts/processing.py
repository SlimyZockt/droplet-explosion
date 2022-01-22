from turtle import st, title
import Scripts.VideoProcessing.VideoProcessing as VideoProcessing
from Scripts.VideoProcessing.Data import SourceData
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def get_data(file: str) -> dict[str, list]:
    source_data: SourceData = VideoProcessing.setup(file, [0, 1])
    data = VideoProcessing.process(source_data, True)

    return data


def _create_plot(ax: Axes, x, y, plt_title: str, label: tuple[str, str]):
    ax.plot(y, x)
    ax.set_title(plt_title)
    ax.set_xlabel(label[0])
    ax.set_ylabel(label[1])


def create_diagrams(data: pd.DataFrame):
    y = data["time_in_s"]
    plt_data = [
        {
            'x': data["droplet_count"],
            'title': "droplet count over time",
            'labels': ("time in s", "count")
        },
        {
            'x': data["added_size"],
            'title': "added droplet area in px over time",
            'labels': ("time in s", "area in px")
        }
    ]
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    for i in range(len(axs)):
        _create_plot(axs[i], plt_data[i]['x'], y, plt_data[i]
                     ['title'], plt_data[i]['labels'])
