import numpy, scipy.signal

def k_weight(x):
    SHELF_B = numpy.array([1.53512485958697, -2.69169618940638, 1.19839281085285], dtype=float)
    SHELF_A = numpy.array([1, -1.69065929318241, 0.73248077421585], dtype=float)
    HP_B = numpy.array([1, -2.0, 1], dtype=float)
    HP_A = numpy.array([1, -1.99004745483398, 0.99007225036621], dtype=float)

    shelved = scipy.signal.lfilter(SHELF_B, SHELF_A, x, axis=0)
    return scipy.signal.lfilter(HP_B, HP_A, shelved, axis=0)

def integrated_lufs(x, rate):
    y = k_weight(x)
    block = int(0.4 * rate)
    Z = []
    start = 0
    hop = int(0.1 * rate)
    while start + block < len(y):
        chunk = y[start:start + block]
        Z.append(numpy.mean(chunk ** 2, axis=0))
        start += hop
    Z = numpy.array(Z)

    power = Z.sum(axis=1)
    lj = -0.691 + 10 * numpy.log10(power)
    abs_mask = lj > -70
    gamma = -0.691 + 10 * numpy.log10(Z[abs_mask].mean(axis=0).sum()) - 10
    mask = abs_mask & (lj > gamma)
    return -0.691 + 10 * numpy.log10(Z[mask].mean(axis=0).sum())