import json
import os
import webview


import matplotlib.pyplot as plt
import pandas as pd


from pathlib import Path

from .modules.util import Util
from .modules.VideoProcessing.VideoProcessing import generate_data_from_src


class Api:

    def setup(self, window: webview.Window):
        self.window = window
        # body of the constructor
    
    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def open_file_dialog(self) -> list[str]:
        file_types = ['Video Files (*.mp4;*.avi;*.mog)']

        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        p = Path(result[0])
        return [p.as_uri(), result[0]]

    def start_analyse(self, files: list[str], debug: bool):
        # if directory:
        #     files = Util.get_file_from_dir()
        #     # click.echo(f"Video Path Dir:, {dir}!")
        # else:
        #     files = [video_path]
        print(f"Video Files: {files}!")

        file = files[0]
        data = generate_data_from_src(file, debug=debug)
        print(data)
        df: pd.DataFrame = pd.DataFrame(data=data)
        # remove last 3 row
        df = df.iloc[:-3]
        Util.create_diagrams(df)
        file_name = os.path.basename(file)
        file_name = os.path.splitext(file_name)[0]

        out_path = f"output/{file_name}"
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        plt.savefig(f"{out_path}/{file_name}.png")
        df.to_csv(f"{out_path}/{file_name}.csv")

        res = df.to_json()
        parsed = json.loads(res)
        
        return parsed
        # return data
