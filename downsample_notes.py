from scipy.io import wavfile
import numpy as np
import parameters
import utilities
import scipy.signal as sig

noteNames = parameters.notes
readpath = 'c:/Users/dough/OneDrive/Documents/AA222_FinalProject/Notes/'
for n in noteNames:
    samplerate, data = wavfile.read(readpath+n+'.wav')
    data = sig.decimate(data,parameters.DOWNSAMPLE_FACTOR).astype(np.int16)
    wavfile.write(readpath+n+"_ds.wav", parameters.DOWNSAMPLE_FS, data) 