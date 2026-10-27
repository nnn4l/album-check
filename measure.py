import soundfile, pathlib

def load_track(file_path):
    sample_array, sample_rate = soundfile.read(file_path)
    duration = len(sample_array) / sample_rate
    channels = 1 if sample_array.ndim == 1 else sample_array.shape[1]
    track_info = {
        "name" : pathlib.Path(file_path).name,
        "sample_rate": sample_rate,
        "channels": channels,
        "duration": duration,
        "sample_array": sample_array,
    }
    return track_info

def scan_folder(folder_path):
    track_list = []
    for file_path in pathlib.Path(folder_path).glob("*"):
        if file_path.is_file():
            track_list.append(load_track(file_path))
    return track_list
    

