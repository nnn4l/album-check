import soundfile, pathlib
import pyloudnorm
import numpy
import scipy.signal

def load_track(file_path):
    sample_array, sample_rate = soundfile.read(file_path)
    OS_sample_array = scipy.signal.resample_poly(sample_array, 4, 1)
    integrated_LUFS = pyloudnorm.Meter(sample_rate).integrated_loudness(sample_array)
    sample_peak = 20 * numpy.log10(numpy.max(numpy.abs(sample_array)))
    true_peak = 20 * numpy.log10(numpy.max(numpy.abs(OS_sample_array)))
    duration = len(sample_array) / sample_rate
    channels = 1 if sample_array.ndim == 1 else sample_array.shape[1]
    track_info = {
        "name" : pathlib.Path(file_path).name,
        "sample_rate": sample_rate,
        "channels": channels,
        "duration": duration,
        "sample_array": sample_array,
        "integrated_LUFS": integrated_LUFS,
        "sample_peak": sample_peak,
        "true_peak": true_peak,
    }
    return track_info

def scan_folder(folder_path):
    track_list = []
    for file_path in pathlib.Path(folder_path).glob("*"):
        if file_path.is_file():
            track_list.append(load_track(file_path))
    return track_list
    

