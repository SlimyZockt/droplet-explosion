import Scripts.VideoProcessing.VideoProcessing as VideoProcessing
from Scripts.VideoProcessing.Data import SourceData

def get_data(file: str) -> dict[str, list]:
    source_data: SourceData = VideoProcessing.setup(file, [0, 1])
    data = VideoProcessing.process(source_data, True)

    return data