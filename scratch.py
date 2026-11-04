import soundfile, pyloudnorm, scipy.signal, meter, numpy

t = numpy.arange(48000) / 48000

s = 0.1 * numpy.sin(2 * numpy.pi * 997 * t)
sine = numpy.column_stack([s, s])

result = meter.k_weight(sine)
print(numpy.abs(result[24000:]).max())