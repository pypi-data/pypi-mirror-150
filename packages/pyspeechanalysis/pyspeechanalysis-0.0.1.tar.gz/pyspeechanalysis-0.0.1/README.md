# PySpeechAnalysis

* Now Support
    - autocorrelation, average_magnitude_difference, bandpass_filter, covariance, discrete_cosine_transfrom, 
    - framming, hamming_window, mel_filter, moving_average, normalize_signal, 
    - pre_emphasis, power_spectrum, standard_deviation 

## Example

How to use

```python
from scipy.io import wavfile
from pyspeechanalysis import SpeechProcessing as SP

inputfile = r'./audio.wav'
[fs, X] = wavfile.read(inputfile)

# PRE-PROCESSING
x = SP.normalize_signal(X, is_figure = True)

y = SP.pre_emphasis(x, is_figure = False)

# FRAMING AND OVERLAPPING
PERCENT = 80
FRAME_MILLISEC = 0.032
frame = SP.set_frame(fs, FRAME_MILLISEC)
signal_vector = SP.framming(y, frame, PERCENT)
```

Check out: https://edocstudio.info