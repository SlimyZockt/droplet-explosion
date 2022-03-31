import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


class Util():

    @staticmethod
    def get_file_from_dir(path: str, extentions: tuple[str]) -> list[str]:
        found_files: list[str] = []
        files = os.listdir(path)
        for file in files:
            if file.endswith(extentions):
                if os.path.isfile(os.path.join(path, file)):
                    found_files.append(os.path.join(path, file))
        return found_files

    @staticmethod
    def create_diagrams(data: pd.DataFrame):
        def create_plot(ax: Axes, x, y, plt_title: str, label: tuple[str, str]):
            ax.plot(y, x)
            ax.set_title(plt_title)
            ax.set_xlabel(label[0])
            ax.set_ylabel(label[1])

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
            create_plot(axs[i], plt_data[i]['x'], y, plt_data[i]
                        ['title'], plt_data[i]['labels'])