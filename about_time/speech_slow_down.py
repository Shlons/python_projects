import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt
import sounddevice as sd


# %% Functions

def FourierCoeffGen(signal):
    # TODO: Implement the FourierCoeffGen function.
    # This function compute signal's Fourier Coefficients.

    FourierCoeff = 0
    N = len(signal)
    FourierCoeff = np.zeros(N, dtype="complex_")
    fourier_transform = 0
    for k in range(0, N):
        for n in range(0, N):
            fourier_transform = fourier_transform + signal[n] * np.exp((-2j * n * k * np.pi) / N)
        FourierCoeff[k] = fourier_transform / N
        fourier_transform = 0
    return FourierCoeff


def DiscreteFourierSeries(FourierCoeff):
    # TODO: Implement the FourierSeries function.
    # This function compute the Discrete Fourier Series from Fourier Coefficients.
    signal = 0
    N = len(FourierCoeff)
    signal = np.zeros(N, dtype="complex_")
    fourier_at_i = 0
    for n in range(0, N):
        for k in range(0, N):
            fourier_at_i = fourier_at_i + FourierCoeff[k] * np.exp(2j * k * np.pi * n / N)
        signal[n] = fourier_at_i
        fourier_at_i = 0
    return signal


#%% import wav file
wav_path = "C:/Users/Barak/PycharmProjects/about_time/jazz.wav"  # Insert your path here, you can pick another wav file!
signal, fs = sf.read(wav_path)
signal=signal[:10*fs] # 10 secounds

plt.figure(1)
plt.title("Input signal Wave")
plt.plot(signal)
#%% Parameters
N = int(512)
step=int(N/4)
kk = 0
M = 3
signal_out = np.zeros(M*len(signal)) # output length
phase_pre = np.ones(N)
last_phase =  np.ones(N)
current_phase = 0
b_k = 0

#%%

print(signal.shape[0] + 1)
for k in range(0, signal.shape[0] + 1 - N , step):
    # Analysis
    print(k)
    x = np.multiply(signal[k:k+N] , np.hamming(N))
    a_k_1 = FourierCoeffGen(x)
    # TODO: 1. Extract the Frame's phase.
    #       2. Find the diff phase
    phase=0
    phase_diff=0
    ############# Your code here ############
    ## (~2 line of code)
    phase=np.divide(a_k_1, np.abs(a_k_1))
    phase_diff=np.divide(phase,phase_pre)
    #########################################

    for n in range(M):
        # Synthesis
        # TODO: 1. Compute the current signal's phase.
        #       2. Compute the output b_k
        #       3. Save the last phase for the next frame

        ############# Your code here ############
        ## (~3 line of code)
        current_phase=np.multiply(phase_diff,last_phase)
        b_k=np.multiply(np.abs(a_k_1), current_phase)
        last_phase=current_phase
        #########################################

        w = np.real(DiscreteFourierSeries(b_k))
        z = np.multiply(w, np.hamming(N))
        signal_out[kk:kk+N] = signal_out[kk:kk+N] + z
        kk = kk + step

    phase_pre = phase


#%% cheack your results
plt.figure(2)
plt.title("Output signal Wave")
plt.plot(signal_out)

output_path = "C:/Users/Barak/PycharmProjects/about_time/jazz_unproductive_out_.wav"  # write your path here!
sf.write(output_path, signal_out, fs)

sd.play(signal_out,fs)
