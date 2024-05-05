from scipy.io import wavfile
import numpy as np

readpath = 'c:/Users/dough/Downloads/F#4_E5.wav'
samplerate, data = wavfile.read(readpath)
data = ((data[:,0]+data[:,1])/2).astype(np.int16) #conv from stereo to mono
note_names = ["F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5"]
num_notes = len(note_names)
note_dur = 4 #sec
samp_per_note = round(note_dur*samplerate)


for i in range(0,num_notes):
    note = data[i*samp_per_note:(i+1)*samp_per_note]
    #wavfile.write(f"{note_names[i]}.wav", samplerate, note)

rest = np.zeros(samp_per_note).astype(np.int16)
wavfile.write(f"rest.wav", samplerate, rest) #silence


