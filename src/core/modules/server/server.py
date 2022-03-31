import os
import json
from functools import wraps

import webview
from flask import Flask, render_template, request, jsonify, send_from_directory

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
    file_types = ['Video Files (*.mp4;*.avi;*.mog)']
    
    files = webview.windows[0].create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
    

    if files and len(files) > 0:
        response = {'status': 'ok', 'files': files}
    else:
        response = {'status': 'cancel'}

    return send_from_directory('UPLOAD_FOLDER', files[0])
