import lpf
import testlpf
import subprocess

#Sampling Freq
Fs = 44100

def pipeline_lpf(signal):
    #Output Signals, using binary coefficients and real coefficients
    cleansigbin, cleansigreal = lpf.main(Fs, signal)
    error_before_write = cleansigreal - cleansigbin

    #Running The Verilog file (lpf)
    subprocess.run(
        ['vvp', 'lpf'], check = True
    )


    inputdata = testlpf.generate_array('input_lpf.txt') #Input to Verilog File
    expected_output = testlpf.generate_array('expected_output_lpf.txt') #Output from Python Filter
    verilog_output = testlpf.generate_array('output_lpf.txt') #Output from Verilog File
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
