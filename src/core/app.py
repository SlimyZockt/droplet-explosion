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


        # return data
