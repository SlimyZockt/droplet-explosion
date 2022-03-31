import threading
import click
import src.core.app as app
import webview
import http.server as server

from src.core.modules.server.server import app as flaskApp


@click.command()
@click.option("-D", "--directory", default=False, is_flag=True,
              help="Use directory for processing multiple videos")
@click.option("-d", "--debgug", default=False, is_flag=True,
              help="Use directory for processing multiple videos")
@click.option("--dev", default=False, is_flag=True,
              help="Use for devolvement with svelte")
def main(directory, debgug, dev):
    api = app.Api()
    source = "public/index.html"
    if dev:
        source = "http://localhost:5000"
    window = webview.create_window('DropletEx Analyse', flaskApp)
    webview.start(setup(api, window), debug=True, http_server=True)
    # start_analyse(video_path, directory, debgug)


def setup(api: app.Api, window: webview.Window):
    api.setup(window)

if __name__ == '__main__':
    print("tewst")
    
    
    # kwargs = {'threaded': True, 'use_reloader': False, 'debug': False}
    # threading.Thread(target=flaskApp.run, daemon=True, kwargs=kwargs)
    # flaskApp.run(port=3000)
    main()
