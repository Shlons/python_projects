import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt
import sounddevice as sd



#%% Functions 

def FourierCoeffGen(signal):
    # This function compute signal's Fourier Coefficients.
    
    FourierCoeff=0
    N = len(signal)
    FourierCoeff = np.zeros(N,dtype="complex_")
    fourier_transform=0
    for k in range(0,N):
        for n in range(0,N):
            fourier_transform=fourier_transform+signal[n]*np.exp((-2j*n*k*np.pi)/N)
        FourierCoeff[k]=fourier_transform/N
        fourier_transform=0
    return FourierCoeff

def  DiscreteFourierSeries(FourierCoeff):
    # This function compute the Discrete Fourier Series from Fourier Coefficients.    
    signal=0
    N=len(FourierCoeff)
    signal=np.zeros(N,dtype="complex_")
    fourier_at_i=0
    for n in range(0, N):
        for k in range(0, N):
            fourier_at_i=fourier_at_i+FourierCoeff[k]*np.exp(2j*k*np.pi*n/N)
        signal[n]=fourier_at_i
        fourier_at_i=0
    return signal

C=9
f_x_1=np.zeros(C)
for i in range(0,C):
    f_x_1[i]=np.cos(2 * np.pi * i / C)
a_k_1=FourierCoeffGen(f_x_1)
#print(a_k_1)
f_x_1_sythesiezed=DiscreteFourierSeries(a_k_1)
#print(f_x_1_sythesiezed)

N_1=5
f_x_2=np.zeros(20*N_1)
for i in range(0,5*N_1):
    f_x_2[i]=1
for i in range(15*N_1+1,20*N_1):
    f_x_2[i] = 1
a_k_2=FourierCoeffGen(f_x_2)
print(a_k_2)
f_x_2_sythesiezed=DiscreteFourierSeries(a_k_2)
plt.plot(a_k_1)
plt.show()
#print(f_x_2_sythesiezed)
