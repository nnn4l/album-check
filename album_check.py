"""album-check: per-track loudness + true peak, album-wide chart.

Nathan writes this. Steps, in order (see README):
  1. list + load each file in the folder (soundfile)
  2. integrated LUFS per track (pyloudnorm) — check one file against ffmpeg
  3. true peak, 4x oversampled (scipy.signal.resample_poly), compare to sample peak
  4. bar chart with -15..-12 band, median line, outlier flags (matplotlib)
"""

import measure

def main(folder_path):
    tracks = list(measure.scan_folder(folder_path))
    for track in tracks:
        print(track["name"], track["integrated_LUFS"], track["sample_peak"], track["true_peak"])

if __name__ == "__main__":
    folder_path = "C:\\Dev\\album-check\\masters"
    main(folder_path)

