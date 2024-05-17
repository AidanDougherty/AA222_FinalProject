import Genome
import Note
import Individual
from scipy.io import wavfile
import numpy as np
import utilities
import random
import copy
import parameters
import matplotlib.pyplot as plt

#Test Synthesize
'''
n1 = Note.Note(noteName='C3',startTime=int(1*parameters.SAMPLE_RATE),duration=int(0.5*parameters.SAMPLE_RATE),velocity=64)
n2 = copy.copy(n1)
n2.shift_start(n1.duration+int(0.001*parameters.SAMPLE_RATE))
gen = Genome.Genome([n1,n2])
s = gen.synthesize()
wavfile.write('test.wav',parameters.SAMPLE_RATE,s)
gen.print_notes()
'''

#Test Crossover
'''
random.seed(34)
scale_down = utilities.make_Cmaj_down()
scale_up = utilities.make_Cmaj_up()

(s1,s2) = scale_down.crossover(scale_up)
s1.print_notes()
s2.print_notes()
'''

#Draw Midi Notes
'''
scale_up = utilities.make_Cmaj_up()
utilities.draw_midi(scale_up)
'''

#Test Mutations
'''
random.seed(222)
scale_up = utilities.make_Cmaj_up()
scale_up.mutate()
utilities.draw_midi(scale_up)
'''

#Test Random Genome Generation
'''
random.seed(69)
gen = Genome.Genome()
utilities.draw_midi(gen)
s = gen.synthesize()
wavfile.write('test.wav',parameters.SAMPLE_RATE,s)
'''

# plot TTLS
'''
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
plt.plot(song)
plt.show()
'''

# plot Midi TTLS
'''
ttls = utilities.make_ttls()
utilities.draw_midi(ttls)
'''

#Spectrograms
'''readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
(f,t,Sxx) = utilities.calc_spectrogram(song)
print(Sxx.shape)
Sxx2 = utilities.normalize_frames(Sxx)
ax = plt.pcolormesh(t, f, Sxx2, shading='gouraud')
plt.axis((0,10,0,600))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

#plt.plot(f,Sxx[:,45])
#plt.xlabel('Frequency [Hz]')
#plt.ylabel('Amplitude')
plt.show()'''


#note frequencies
'''readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
(f,t,Sxx) = utilities.calc_spectrogram(song)
print(Sxx.shape)
#print(parameters.NOTE_INDICES)
plt.stem(f)
plt.axis((0,650,0,700))
plt.hlines(parameters.note_freqs,0,650,'r')
plt.ylabel('Frequency [Hz]')
plt.show()'''

#Calc Note Amplitudes + Test Fitness function
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
(f,t,Sxx) = utilities.calc_spectrogram(song)
print(Sxx.shape)
Sxx = utilities.normalize_frames(Sxx)
target_amps = utilities.eval_note_amplitudes(Sxx)
#ax = plt.pcolormesh(t, np.arange(1,38), amps, shading='gouraud')
#plt.show()

ttls_gen = utilities.make_ttls()
Iperf = Individual.Individual(genome=ttls_gen)
cmaj_gen = utilities.make_Cmaj_up()
Icmaj = Individual.Individual(genome=cmaj_gen)
Irand = Individual.Individual()
quiet_gen = Genome.Genome(noteList=[])
Irest = Individual.Individual(quiet_gen)
print(f"Ideal Score: {Iperf.evaluate_self(target_amps)}")
print(f"CMajor Score: {Icmaj.evaluate_self(target_amps)}")
print(f"Random Score: {Irand.evaluate_self(target_amps)}")
print(f"Silent Score: {Irest.evaluate_self(target_amps)}")
#utilities.draw_midi(Irand.genome)