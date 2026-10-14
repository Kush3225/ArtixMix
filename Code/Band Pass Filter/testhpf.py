import numpy as np
import matplotlib.pyplot as plt


def generate_array(filename):

    with open(filename, 'r') as file:
        output = [line.strip() for line in file]

    output = [
        int(x, 2) - (1 << 24) if x[0] == '1' else int(x, 2)
        for x in output
    ]

    output = np.array(output)/2**23

    return output


def fft(signal):

    signalf = np.abs(np.fft.fft(signal))

    return signalf