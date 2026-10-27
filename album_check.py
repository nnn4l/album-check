"""album-check: per-track loudness + true peak, album-wide chart.

Nathan writes this. Steps, in order (see README):
  1. list + load each file in the folder (soundfile)
  2. integrated LUFS per track (pyloudnorm) — check one file against ffmpeg
  3. true peak, 4x oversampled (scipy.signal.resample_poly), compare to sample peak
  4. bar chart with -15..-12 band, median line, outlier flags (matplotlib)
"""
