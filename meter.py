import numpy, scipy.signal

def k_weight(x):
    SHELF_B = numpy.array([1.53512485958697, -2.69169618940638, 1.19839281085285], dtype=float)
    SHELF_A = numpy.array([1, -1.69065929318241, 0.73248077421585], dtype=float)
    HP_B = numpy.array([1, -2.0, 1], dtype=float)
    HP_A = numpy.array([1, -1.99004745483398, 0.99007225036621], dtype=float)

    shelved = scipy.signal.lfilter(SHELF_B, SHELF_A, x, axis=0)
    return scipy.signal.lfilter(HP_B, HP_A, shelved, axis=0)