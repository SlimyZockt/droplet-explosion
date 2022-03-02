from multiprocessing.dummy import Array
from Scripts.processing import create_diagrams
from Scripts.VideoProcessing.VideoProcessing import generate_data_from_src
import click
import os
import pandas as pd
import matplotlib.pyplot as plt


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
@click.option("-D", "--directory", default=False, is_flag=True,
              help="Use directory for processing multiple videos")
@click.option("-d", "--debgug", default=False, is_flag=True,
              help="Use directory for processing multiple videos")
def main(video_path, directory, debgug):
    files: list[str] = []
    if directory:
        files = _get_file_from_dir(video_path, (".mp4", ".avi"))
        # click.echo(f"Video Path Dir:, {dir}!")
    else:
        files.append(video_path)
    click.echo(f"Video Files: {files}!")

    for file in files:
        data = generate_data_from_src(file, debug=debgug)
        print(data)
        df = pd.DataFrame(data=data)
        # remove last row
        df = df.iloc[:-3]
        print(df)
        create_diagrams(df)
        file_name = os.path.basename(file)
        file_name = os.path.splitext(file_name)[0]

        out_path = f"output/{file_name}"
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        plt.savefig(f"{out_path}/{file_name}.png")
        df.to_csv(f"{out_path}/{file_name}.csv")
        # print(file)


if __name__ == '__main__':
    main()