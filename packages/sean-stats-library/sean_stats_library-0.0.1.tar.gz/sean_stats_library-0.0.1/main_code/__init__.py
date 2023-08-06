import math

def avg(work):
    total = 0
    for i in range(len(work)):
        total += work[i]
    out = total / len(work)
    return out


def sample_variance(work):
    total = 0
    for k in range(len(work)):
        total += work[k]
    avg_x = total / len(work)
    num = 0
    for n in range(len(work)):
        num += (work[n] - avg_x)**2
    variance = num / (len(work) - 1)
    return variance


def sample_standard_deviation(samp_variance):
    deviation = math.sqrt(samp_variance)
    return deviation



def error(work, dev):
    err = dev / math.sqrt(len(work))
    return err