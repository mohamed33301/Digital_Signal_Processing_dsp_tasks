import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from comparesignals import SignalSamplesAreEqual


def read_signal(text_file):
    with open(text_file, 'r') as file:
        signal = []
        values = []
        for line in file:
            words = line.strip().split()
            if len(words) == 1:
                values.append(int(words[0]))
            if len(words) == 2:
                pair = [int(words[0]), float(words[1])]
                signal.append(pair)
    signal = np.array(signal).reshape(-1, 2)
    return signal


def display_continuous(signal):
    plt.plot(signal[:, 0], signal[:, 1], label='Continuous Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.legend()
    plt.show()


def display_disc(signal):
    plt.stem(signal[:, 0], signal[:, 1], basefmt=" ", label='Discrete Samples')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()


def sin_signal(amplitude, phase_shift, analog_frequency, sampling_frequency):
    t = np.linspace(0, 1, int(sampling_frequency), endpoint=False).reshape(-1, 1)
    signal = amplitude * np.sin(2 * np.pi * analog_frequency * t + phase_shift)

    return np.concatenate((t, signal), axis=1)


def cos_signal(amplitude, phase_shift, analog_frequency, sampling_frequency):
    t = np.linspace(0, 1, int(sampling_frequency), endpoint=False).reshape(-1, 1)
    signal = amplitude * np.cos(2 * np.pi * analog_frequency * t + phase_shift)

    return np.concatenate((t, signal), axis=1)


