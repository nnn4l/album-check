import soundfile, pyloudnorm, scipy.signal, meter

data, rate = soundfile.read("C:/Dev/album-check/masters/running.wav")
data48k = scipy.signal.resample_poly(data, 160, 147)
print("resampled:", pyloudnorm.Meter(48000, filter_class="DeMan").integrated_loudness(data48k))
print("original:", pyloudnorm.Meter(44100, filter_class="DeMan").integrated_loudness(data))

print(meter.integrated_lufs(data48k, 48000))