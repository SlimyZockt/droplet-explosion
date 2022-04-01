import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import webview
from flask import Flask, render_template, send_from_directory, request

from ..util import Util
from ..VideoProcessing.VideoProcessing import generate_data_from_src

gui_dir = '../../../../public'

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mog'}

app = Flask(
    __name__, static_url_path=f'/{gui_dir}',
    template_folder=f'{gui_dir}',
    static_folder=f'{gui_dir}'
    )
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def landing():
    """
    Render index.html. Initialization is performed asynchronously in initialize() function
    """
    return render_template('index.html', token=webview.token)


@app.route("/<path:path>")
def home(path):
    return send_from_directory(gui_dir, path)


@app.route('/choose/path', methods=['POST'])
def choose_path():
    '''
    Invoke a folder selection dialog here
    :return:
    ''' 
    if request.method != 'POST':
        return {}
    file_types = ['Video Files (*.mp4;*.avi;*.mog)']

    files = webview.windows[0].create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)

    if files and len(files) > 0:
        response = {'status': 'ok', 'files': files}
    else:
        response = {'status': 'cancel'}

    return response
    # return send_from_directory('UPLOAD_FOLDER', files[0])


@app.route('/analyse/video', methods=['POST'])
def analyse_video():

    if request.method != 'POST':
        return {}

    files = request.form['files']
    debug = request.form['debug']

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
