from Scripts.processing import get_data

import click
import os


def _get_file_from_dir(path: str, extentions: tuple[str]) -> list[str]:
    found_files: list[str] = []
    files = os.listdir(path)
    for file in files:
        if file.endswith(extentions):
            if os.path.isfile(os.path.join(path, file)):
                found_files.append(os.path.join(path, file))
    return found_files

@click.command()
@click.argument('video_path')
@click.option( "-D", "--directory",default=False,is_flag=True, help="Use directory for processing multiple videos")
@click.option( "-d", "--debgug",default=False, help="Use directory for processing multiple videos")
def process_video(video_path, directory, debgug):
    files: list[str] = []
    if directory:
        files = _get_file_from_dir(video_path, (".mp4",".avi"))
        # click.echo(f"Video Path Dir:, {dir}!")
    else:
        files.append(video_path)
    click.echo(f"Video Files: {files}!")

    for file in files:
        data = get_data(file)

if __name__ == '__main__':
    process_video()