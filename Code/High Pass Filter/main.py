import hpf
import testhpf
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import textwrap
import os
import shutil

#Sampling Freq
Fs = 44100

#Time Axis
#timevector = np.linspace(0, 1/5000, Fs, endpoint= False)
timevector = np.arange(Fs)/Fs

#Freq Axis
Numberofsamples = Fs
fstep = Fs/Numberofsamples
freqvector = np.linspace(0, (Numberofsamples-1)*fstep , Numberofsamples)

#Compiling Verilog File
subprocess.run(
    ['iverilog', '-o', 'hpf', 'hpf.v'], check = True
)



def pipline(signal):
    #Output Signals, using binary coefficients and real coefficients
    cleansigbin, cleansigreal = hpf.main(Fs, signal)
    error_before_write = cleansigreal - cleansigbin

    #Running The Verilog file (hpf)
    subprocess.run(
        ['vvp', 'hpf'], check = True
    )


    inputdata = testhpf.generate_array('input.txt') #Input to Verilog File
    expected_output = testhpf.generate_array('expected_output.txt') #Output from Python Filter
    verilog_output = testhpf.generate_array('output.txt') #Output from Verilog File
    time_domain_error = expected_output - verilog_output

    inputf = testhpf.fft(inputdata) #FFT of Input Signal
    expected_outputf = testhpf.fft(expected_output) #FFT of Python's Output
    verilog_outputf = testhpf.fft(verilog_output) #FFT of Verilog's Output
    errorf = expected_outputf - verilog_outputf

    processed_signal = {
        "noisysig" : signal,
        "cleansigbin" : cleansigbin,
        "cleansigreal" : cleansigreal,
        "error_before_write" : error_before_write,

        "inputdata" : inputdata,
        "expected_output" : expected_output,
        "verilog_output" : verilog_output,
        "time_domain_error" : time_domain_error,

        "inputf" : inputf,
        "expected_outputf" : expected_outputf,
        "verilog_outputf" : verilog_outputf,
        "errorf" : errorf
    }

    return processed_signal

noisysig =  0.5*(np.sin(2*np.pi*5*1000*timevector)) + 0.25
unit_impulse = np.zeros(len(timevector))
unit_impulse[0] = 0.99

clean_noisy = pipline(noisysig)
impulse_response = pipline(unit_impulse)



fig, ax = plt.subplots(3, 4, figsize=(20, 12), layout="constrained")
ax[0, 0].plot(timevector[0:99], clean_noisy["noisysig"][0:99]); ax[0, 0].set_title("Noisy input")
ax[0, 1].plot(timevector[0:99], clean_noisy["cleansigbin"][0:99]); ax[0, 1].set_title("Filtered (normalized by DC gain), Bin")
ax[0, 2].plot(timevector[0:99], clean_noisy["cleansigreal"][0:99]); ax[0, 2].set_title("Filtered (normalized by DC gain), Real")
ax[0, 3].plot(timevector[0:99], clean_noisy["error_before_write"][0:99]); ax[0, 3].set_title("Error")

ax[1, 0].plot(timevector[0:99], clean_noisy["inputdata"][0:99]); ax[1, 0].set_title("Input")
ax[1, 1].plot(timevector[0:99], clean_noisy["expected_output"][0:99]); ax[1, 1].set_title("Expected Output")
ax[1, 2].plot(timevector[0:99], clean_noisy["verilog_output"][0:99]); ax[1, 2].set_title("Verilog Output")
ax[1, 3].plot(timevector[0:99], clean_noisy["time_domain_error"][0:99]); ax[1, 3].set_title("Error")

ax[2, 0].semilogx(freqvector[1: int(Fs/2)], impulse_response["inputf"][1:int(Fs/2)]); ax[2, 0].set_title("Input Frequnecies")
ax[2, 1].semilogx(freqvector[1: int(Fs/2)], impulse_response["expected_outputf"][1:int(Fs/2)]); ax[2, 1].set_title("Expected Frequency Response")
ax[2, 2].semilogx(freqvector[1: int(Fs/2)], impulse_response["verilog_outputf"][1:int(Fs/2)]); ax[2, 2].set_title("Verilog Frequency Response")
ax[2, 3].semilogx(freqvector[1: int(Fs/2)], impulse_response["errorf"][1:int(Fs/2)]); ax[2, 3].set_title("Error in Frequency Response")


for a in ax.flat:
    a.set_title(textwrap.fill(a.get_title(), width=28), fontsize=9)

fig.suptitle("DSP Biquad High Pass Filter — Complete Analysis", fontsize=14)
plt.show() 

os.remove('hpf')
os.remove('input.txt')
os.remove('expected_output.txt')
os.remove('output.txt')
shutil.rmtree('__pycache__')