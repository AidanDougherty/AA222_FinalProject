import Note
import Genome
import utilities
import parameters
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
from scipy.io import wavfile

'''b = Note.Note("B3",1*parameters.SAMPLE_RATE,4*parameters.SAMPLE_RATE,64)
c = Note.Note("C4",1*parameters.SAMPLE_RATE,4*parameters.SAMPLE_RATE,64)
genb = Genome.Genome([b])
genc = Genome.Genome([c])
b3 = genb.synthesize()
c4 = genc.synthesize()
b3_down = utilities.downsample(b3)
c4_down = utilities.downsample(c4)
(f,t,Sxxb) = utilities.calc_spectrogram(b3_down)
(f,t,Sxxc) = utilities.calc_spectrogram(c4_down)
print(np.max(Sxxb))
print(np.max(Sxxc))

genbc = Genome.Genome([b,c])
bc = genbc.synthesize()
bc_down = utilities.downsample(bc)
(f,t,Sxxbc) = utilities.calc_spectrogram(bc_down)
ax = plt.pcolormesh(t,f,Sxxbc, shading='gouraud')
plt.axis((0,10,0,600))
plt.show()'''
#wavfile.write('b3_test.wav',parameters.SAMPLE_RATE,b3)

#Note rescaling
notes = parameters.notes

total = 0
count = 0
peaks = []
for noteName in notes:
    n = Note.Note(noteName,1*parameters.SAMPLE_RATE,4*parameters.SAMPLE_RATE,64)
    gen = Genome.Genome([n])
    syn = gen.synthesize()
    ds = utilities.downsample(syn)
    (f,t,Sxx) = utilities.calc_spectrogram(ds)
    amps = utilities.eval_note_amplitudes(Sxx)
    peaks.append(np.max(amps))
    total+=np.max(amps)
    count+=1
avg = total/count
print(f"avg: {avg}")
print(f"peaks: {peaks}")
rescaling = np.sqrt(avg/np.array(peaks))
print(rescaling)
