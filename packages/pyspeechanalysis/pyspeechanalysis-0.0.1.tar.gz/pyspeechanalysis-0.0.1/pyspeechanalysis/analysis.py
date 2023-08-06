import math
import numpy as np
import matplotlib.pyplot as plt


class SpeechProcessing:


    @staticmethod
    def set_frame(fs, millisec=0.032):
        return int(math.floor(millisec * fs))
        
    @staticmethod
    def pre_emphasis(signal, is_figure=True):
        y = []
        y.append(signal[0])
        for n in range(1,len(signal)):
            y.append(signal[n] - 0.97 * signal[n-1])
        if is_figure == True:
            plt.plot(y)
            plt.show()
        return y
    
    @staticmethod
    def hamming_window(x):
        w = []
        N = len(x) - 1
        for n in x:
            w.append(0.54 - 0.46 * math.cos( (2* math.pi * n) / N))
        return w
    
    @staticmethod
    def framming(signal, frame, percentShift=80):
        N = len(signal)
        shift = int(math.floor(percentShift*frame/100))
        total_frame = int(math.ceil((N-shift) / shift))
        frame_vector = []
        for l in range(0, total_frame):
            row = []
            for n in range(0,frame):
                row.append( signal[shift*l+n] )
            frame_vector.append(row)
        return frame_vector
    
    @staticmethod
    def moving_average(signal, move):
        smooth_signal = []
        N = len(signal)
        for n in range(1,move+1):
            signal.append(0)
        for n in range(0,N):
            smoothing = 0
            for m in range(1,move+1):
                smoothing += signal[n + m]
            smooth_signal.append(smoothing/move)
        return smooth_signal
    
    @staticmethod
    def standard_deviation(signal):
        mean = sum(signal)/len(signal)
        distance = []
        for x in signal:
            distance.append(math.pow(x - mean,2))
        sum_energy = sum(distance)
        standard_deviation = math.sqrt(sum_energy/len(signal))
        return (sum_energy, standard_deviation)
    
    @staticmethod
    def normalize_signal(signal, is_figure=True):
        x = np.array(signal)/np.amax(signal)
        if is_figure == True:
            plt.plot(x)
            plt.show()
        return x

    @staticmethod
    def power_spectrum(signal):
        fft = np.fft.fft(signal)
        N = len(signal)/2
        power_spectrum = [math.pow(abs(fft[n]), 2) for n in range(0, math.floor(N))]
        return (1/N)*np.array(power_spectrum)
    
    @staticmethod
    def mel_filter(freq_low, freq_high, channel, N, is_figure_filter=True):
        channel+=2
        mel_low = 1125 * math.log(1+freq_low/700)
        mel_high = 1125 * math.log(1+freq_high/700)
        mel = np.linspace(mel_low, mel_high, channel)
        h = [ 700*(math.exp(n/1125)-1) for n in mel]
        freq = [math.floor( ((N+1)*h[n])/(freq_high*2) ) for n in range(0,channel)]
        last_freq = freq[-1]
        mel_axis = np.linspace(0, freq_high, last_freq)
        mel_tri_filter = []
        for c in range(0,channel-2):
            triangular_filter = []
            for k in range(1,last_freq+1):
                m = c+1
                if k < freq[m-1]:
                    triangular_filter.append(0)
                elif k >= freq[m-1] and k <= freq[m]:
                    triangular_filter.append((k-freq[m-1])/(freq[m]-freq[m-1]))
                elif k <= freq[m+1] and k >= freq[m]:
                    triangular_filter.append((freq[m+1]-k)/(freq[m+1]-freq[m]))
                elif k > freq[m+1]:
                    triangular_filter.append(0)
            mel_tri_filter.append(triangular_filter)
        if is_figure_filter == True:
            for n in range(0,len(mel_tri_filter)):
                plt.plot(mel_axis, mel_tri_filter[n][:])
            plt.show()
        return (mel_tri_filter, mel_axis)
        
    @staticmethod
    def bandpass_filter(power_spectrum, filter):
        filter_signal = []
        [x, y] = np.shape(filter)
        for n in range(0,x):
            signal = 0
            for m in range(0,y-1):
                signal += power_spectrum[m]*filter[n][m]
            filter_signal.append(signal)
        return filter_signal

    @staticmethod 
    def discrete_cosine_transfrom(filter_signal, order):
        MFCC = []
        mel_freq_log = [ np.log(x) for x in filter_signal ]
        N = len(mel_freq_log)
        for k in range(0,order):
            mel_freq_coe = 0
            for n in range(0,N):
                mel_freq_coe+=mel_freq_log[n]*math.cos(k*(n-0.5)*(math.pi/N))
            MFCC.append(mel_freq_coe)
        return MFCC
    
    @staticmethod
    def autocorrelation(signal, K):
        N = len(signal)
        autocorre_j = []
        [I, J] = K
        for j in range(J):
            autocorre_i = []
            for i in range(I):
                IJ = abs(i-j)
                r = 0
                for n in range(N-1-IJ):
                    r+=signal[n]*signal[n + abs(i-j)]
                autocorre_i.append(r)
            autocorre_j.append(autocorre_i)
        return autocorre_j
    
    @staticmethod
    def covariance(signal, K):
        N = len(signal)
        covariance_j = []
        [I, J] = K
        for j in range(J):
            covariance_i = []
            for i in range(I):
                c = 0
                for n in range(N-1):
                    c+=signal[n - i]*signal[n - j]
                covariance_i.append(c)
            covariance_j.append(covariance_i)
        return covariance_j
    
    @staticmethod
    def average_magnitude_difference(signal, K):
        N = len(signal)
        linear_predictive = []
        for k in range(1,K):
            amd = 0
            for m in range(k,N):
                amd += abs(signal[m] - signal[m-k])
            linear_predictive.append(amd)
        return linear_predictive