import numpy as np
import matplotlib.pyplot as plt


#making the real numbers signed

def to_signed(val, bits=18):
    if val & (1 << (bits - 1)):
        val -= 1 << bits
    return val



#Making the filter

def biquad(x, b, a):
    """y[n] = b0 x[n] + b1 x[n-1] + b2 x[n-2] - a1 y[n-1] - a2 y[n-2]"""
    y = np.zeros_like(x, dtype=float)
    for n in range(len(x)):
        y[n] = b[0] * x[n]
        if n >= 1:
            y[n] += b[1] * x[n-1] - a[0] * y[n-1]
        if n >= 2:
            y[n] += b[2] * x[n-2] - a[1] * y[n-2]
    return y



#_________ Writing The outputs in binary in a file__________

Q_FRAC_BITS = 23
Q_WORD_BITS = 24

def decimal_to_q1_23(x):
    """Float -> 24-bit two's complement Q1.23 string."""
    fixed = int(round(x * (1 << Q_FRAC_BITS)))
    return format(fixed & ((1 << Q_WORD_BITS) - 1), f'0{Q_WORD_BITS}b')

def write_q1_23_file(filename, samples):
    with open(filename, 'w') as f:
        for s in samples:
            f.write(decimal_to_q1_23(s) + '\n')


def main(Fs, noisysig):

    

    #Filter Coefficients

    FRAC_BITS = 16           #Q2.16
    scale = 2.0 ** FRAC_BITS

    #Fixed Point arthmetic
    bbin = np.array([to_signed(0x00014), to_signed(0x00028), to_signed(0x00014)]) / scale
    abin = np.array([to_signed(0x20CE5), to_signed(0x0F36C)]) / scale   

    #Real i.e. Theoretical Values of filter coefficients
    breal = np.array([0.000309354, 0.000618708, 0.000309354])
    areal = np.array([-1.9496374, 0.9508749])

    cleansigbin = biquad(noisysig, bbin, abin)
    cleansigreal = biquad(noisysig, breal, areal)

    #Testing Max and Min Values 
    print("Maximum and minimum input to LPF -> ", max(noisysig), min(noisysig))
    print("Maximum and minimum output of LPF -> ", max(cleansigbin), min(cleansigbin))

    

    write_q1_23_file('input.txt', noisysig)
    write_q1_23_file('expected_output.txt', cleansigbin)

    return cleansigbin, cleansigreal


