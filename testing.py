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
import pickle
import time

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

'''ttls = utilities.make_ttls()
utilities.draw_midi(ttls)
plt.title("Ground Truth Melody")
plt.show()'''

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
print(song.shape)
(f,t,Sxx) = utilities.calc_spectrogram(song)
print(Sxx.shape)
print(t.shape)
target_Sxx = utilities.normalize_frames(Sxx)
#target_Sxx = Sxx
#target_Sxx = utilities.attenuate_harmonics(target_Sxx)

target_amps = utilities.eval_note_amplitudes(target_Sxx)

print(target_amps.shape)
'''fig,ax = plt.subplots()
ax.pcolormesh(t, np.arange(1,38), target_amps, shading='gouraud')
ax.set_ylabel("Note Frequency")
ax.set_xlabel("Time (s)")
ax.set_title("Ground Truth Spectrogram")
plt.show()'''
#target_amps = Sxx
#ax = plt.pcolormesh(t, np.arange(1,38), amps, shading='gouraud')
#plt.show()
#print(target_amps)
ttls_gen = utilities.make_ttls()
Iperf = Individual.Individual(genome=ttls_gen)
cmaj_gen = utilities.make_Cmaj_up()
Icmaj = Individual.Individual(genome=cmaj_gen)
Irand = Individual.Individual()
quiet_gen = Genome.Genome(noteList=[])
Irest = Individual.Individual(quiet_gen)
approx_genome = utilities.fit_notes(target_amps)
Iapprox = Individual.Individual(approx_genome)
print(f"Ideal Score: {Iperf.evaluate_self(target_amps)}")
print(f"CMajor Score: {Icmaj.evaluate_self(target_amps)}")
print(f"Random Score: {Irand.evaluate_self(target_amps)}")
print(f"Silent Score: {Irest.evaluate_self(target_amps)}")
print(f"Estimation Score: {Iapprox.evaluate_self(target_amps)}")

(f,t,ttls_Sxx) = utilities.calc_spectrogram(utilities.downsample(ttls_gen.synthesize()))
'''ttls_Sxx = utilities.rescale_to_target(ttls_Sxx,target_Sxx)
plt.plot(f,target_Sxx[:,15],color='blue')
plt.plot(f,ttls_Sxx[:,15],color='red')
plt.show()'''

ttls_amps = utilities.eval_note_amplitudes(ttls_Sxx)
ttls_amps = utilities.rescale_to_target(ttls_amps,target_amps)
ns = np.arange(1,38)
plt.plot(ns,target_amps[:,156],color='blue')
plt.plot(ns,ttls_amps[:,156],color='red')
plt.show()
#utilities.draw_midi(Irand.genome)'''

#plotting ga test data
'''with open('FFT_noNorm_200gen_freqpen.pkl','rb') as f:  # Python 3: open(..., 'rb')
    obj0, obj1 = pickle.load(f)

plt.plot(obj1)
plt.xlabel("Generation")
plt.ylabel("Fitness")

plt.title("Fitness vs Generation, No Normalization, FFT and Freq Penalty Based")
plt.show()'''

#Time downsampling + synthesis vs FFT
#downsampling 100 random genomes - 2.456 seconds
#100 spectrograms of downsampled genomes - 1.710 seconds
'''ph_list = []
for i in range(0,100):
    gen = Genome.Genome()
    phenotype = gen.synthesize()
    #phenotype = utilities.downsample(phenotype)
    ph_list.append(phenotype)

start_time = time.time()
for ph in ph_list:
#    spec = utilities.calc_spectrogram(ph)
    ph = utilities.downsample(ph)
print("--- %s seconds ---" % (time.time() - start_time))
'''