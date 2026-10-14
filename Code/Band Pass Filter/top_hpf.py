import hpf
import testhpf
import subprocess

#Sampling Freq
Fs = 44100

def pipeline_hpf(signal):
    #Output Signals, using binary coefficients and real coefficients
    cleansigbin, cleansigreal = hpf.main(Fs, signal)
    error_before_write = cleansigreal - cleansigbin

    #Running The Verilog file (hpf)
    subprocess.run(
        ['vvp', 'hpf'], check = True
    )


    inputdata = testhpf.generate_array('input_hpf.txt') #Input to Verilog File
    expected_output = testhpf.generate_array('expected_output_hpf.txt') #Output from Python Filter
    verilog_output = testhpf.generate_array('output_hpf.txt') #Output from Verilog File
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

