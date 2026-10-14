import lpf
import testlpf
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import textwrap
import os
import shutil

#Sampling Freq
Fs = 44100

#Time Axis
timevector = np.arange(Fs)/Fs

#Freq Axis
Numberofsamples = Fs
fstep = Fs/Numberofsamples
freqvector = np.linspace(0, (Numberofsamples-1)*fstep , Numberofsamples)

#Compiling Verilog File
subprocess.run(
    ['iverilog', '-o', 'lpf', 'lpf.v'], check = True
)



def pipeline(signal):
    #Output Signals, using binary coefficients and real coefficients
    cleansigbin, cleansigreal = lpf.main(Fs, signal)
    error_before_write = cleansigreal - cleansigbin

    #Running The Verilog file (lpf)
    subprocess.run(
        ['vvp', 'lpf'], check = True
    )


    inputdata = testlpf.generate_array('input.txt') #Input to Verilog File
    expected_output = testlpf.generate_array('expected_output.txt') #Output from Python Filter
    verilog_output = testlpf.generate_array('output.txt') #Output from Verilog File
    time_domain_error = expected_output - verilog_output

    inputf = testlpf.fft(inputdata) #FFT of Input Signal
    expected_outputf = testlpf.fft(expected_output) #FFT of Python's Output
    verilog_outputf = testlpf.fft(verilog_output) #FFT of Verilog's Output
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


noisysig =  0.5*(np.sin(2*timevector*np.pi*1) + 0.15*np.random.randn(len(timevector)))
unit_impulse = np.zeros(len(timevector))
unit_impulse[0] = 0.99

clean_noisy = pipeline(noisysig)
impulse_response = pipeline(unit_impulse)


fig, ax = plt.subplots(3, 4, figsize=(20, 12), layout="constrained")
ax[0, 0].plot(timevector, clean_noisy["noisysig"]); ax[0, 0].set_title("Noisy input")
ax[0, 1].plot(timevector, clean_noisy["cleansigbin"]); ax[0, 1].set_title("Filtered (normalized by DC gain), Bin")
ax[0, 2].plot(timevector, clean_noisy["cleansigreal"]); ax[0, 2].set_title("Filtered (normalized by DC gain), Real")
ax[0, 3].plot(timevector, clean_noisy["error_before_write"]); ax[0, 3].set_title("Error")



ax[1, 0].plot(timevector, clean_noisy["inputdata"]); ax[1, 0].set_title("Input")
ax[1, 1].plot(timevector, clean_noisy["expected_output"]); ax[1, 1].set_title("Expected Output")
ax[1, 2].plot(timevector, clean_noisy["verilog_output"]); ax[1, 2].set_title("Verilog Output")
ax[1, 3].plot(timevector, clean_noisy["time_domain_error"]); ax[1, 3].set_title("Error")



ax[2, 0].semilogx(freqvector[1: int(Fs/2)], impulse_response["inputf"][1:int(Fs/2)]); ax[2, 0].set_title("Input Frequnecies")
ax[2, 1].semilogx(freqvector[1: int(Fs/2)], impulse_response["expected_outputf"][1:int(Fs/2)]); ax[2, 1].set_title("Expected Frequency Response")
ax[2, 2].semilogx(freqvector[1: int(Fs/2)], impulse_response["verilog_outputf"][1:int(Fs/2)]); ax[2, 2].set_title("Verilog Frequency Response")
ax[2, 3].semilogx(freqvector[1: int(Fs/2)], impulse_response["errorf"][1:int(Fs/2)]); ax[2, 3].set_title("Error in Frequency Response")

for a in ax.flat:
    a.set_title(textwrap.fill(a.get_title(), width=28), fontsize=9)

fig.suptitle("DSP Biquad Filter — Complete Analysis", fontsize=14)
plt.show() 

os.remove('lpf')
os.remove('input.txt')
os.remove('expected_output.txt')
os.remove('output.txt')
shutil.rmtree('__pycache__')