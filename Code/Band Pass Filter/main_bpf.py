import top_lpf
import top_hpf
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import textwrap
import os
import shutil


#Sampling Freq
Fs = 44100

#Time Axis
#timevector = np.linspace(0, 1/500, Fs, endpoint= False)
timevector = np.arange(Fs)/Fs

#Freq Axis
Numberofsamples = Fs
fstep = Fs/Numberofsamples
freqvector = np.linspace(0, (Numberofsamples-1)*fstep , Numberofsamples)

#Compiling Verilog File
subprocess.run(
    ['iverilog', '-o', 'hpf', 'hpf.v'], check = True
)

subprocess.run(
    ['iverilog', '-o', 'lpf', 'lpf.v'], check = True
)


def pipeline_bpf(signal):

    hpf_output = top_hpf.pipeline_hpf(signal)
    bpf_output = top_lpf.pipeline_lpf((hpf_output['verilog_output']))

    return bpf_output


noisysig =  0.5*(np.sin(2*timevector*np.pi*1) + 0.15*np.random.randn(len(timevector)))
unit_impulse = np.zeros(len(timevector))
unit_impulse[0] = 0.99
unit_impulsef = np.abs(np.fft.fft(unit_impulse))

clean_noisy = pipeline_bpf(noisysig)
impulse_response = pipeline_bpf(unit_impulse)


fig, ax = plt.subplots(3, 4, figsize=(20, 12), layout="constrained")
ax[0, 0].plot(timevector[0:99], noisysig[0:99]); ax[0, 0].set_title("Noisy input")
ax[0, 1].plot(timevector[0:99], clean_noisy["cleansigbin"][0:99]); ax[0, 1].set_title("Filtered (normalized by DC gain), Bin")
ax[0, 2].plot(timevector[0:99], clean_noisy["cleansigreal"][0:99]); ax[0, 2].set_title("Filtered (normalized by DC gain), Real")
ax[0, 3].plot(timevector[0:99], clean_noisy["error_before_write"][0:99]); ax[0, 3].set_title("Error")



ax[1, 0].plot(timevector[0:99], clean_noisy["inputdata"][0:99]); ax[1, 0].set_title("Input")
ax[1, 1].plot(timevector[0:99], clean_noisy["expected_output"][0:99]); ax[1, 1].set_title("Expected Output")
ax[1, 2].plot(timevector[0:99], clean_noisy["verilog_output"][0:99]); ax[1, 2].set_title("Verilog Output")
ax[1, 3].plot(timevector[0:99], clean_noisy["time_domain_error"][0:99]); ax[1, 3].set_title("Error")



ax[2, 0].semilogx(freqvector[1: int(Fs/2)], unit_impulsef[1:int(Fs/2)]); ax[2, 0].set_title("Input Frequnecies")
ax[2, 1].semilogx(freqvector[1: int(Fs/2)], impulse_response["expected_outputf"][1:int(Fs/2)]); ax[2, 1].set_title("Expected Frequency Response")
ax[2, 2].semilogx(freqvector[1: int(Fs/2)], impulse_response["verilog_outputf"][1:int(Fs/2)]); ax[2, 2].set_title("Verilog Frequency Response")
ax[2, 3].semilogx(freqvector[1: int(Fs/2)], impulse_response["errorf"][1:int(Fs/2)]); ax[2, 3].set_title("Error in Frequency Response")


for a in ax.flat:
    a.set_title(textwrap.fill(a.get_title(), width=28), fontsize=9)

fig.suptitle("DSP Biquad Filter — Complete Analysis", fontsize=14)
plt.show() 

os.remove('hpf')
os.remove('input_hpf.txt')
os.remove('expected_output_hpf.txt')
os.remove('output_hpf.txt')
os.remove('lpf')
os.remove('input_lpf.txt')
os.remove('expected_output_lpf.txt')
os.remove('output_lpf.txt')
shutil.rmtree('__pycache__')