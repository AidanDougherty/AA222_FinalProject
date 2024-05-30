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

#Test note fitting
'''readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
print(song.shape)
(f,t,Sxx) = utilities.calc_spectrogram(song)
print(Sxx.shape)
target_Sxx = utilities.normalize_frames(Sxx)
#target_Sxx = Sxx
#target_Sxx = utilities.attenuate_harmonics(target_Sxx)

target_amps = utilities.eval_note_amplitudes(target_Sxx)
print(target_amps.shape)
approx_target_gen = utilities.fit_notes(target_amps)
#utilities.draw_midi(approx_target_gen)
s = approx_target_gen.synthesize()
#wavfile.write('approx.wav',parameters.SAMPLE_RATE,s)
s = utilities.downsample(s)
(f,t,Sxx2) = utilities.calc_spectrogram(s)
approx_amps = utilities.eval_note_amplitudes(Sxx2)
ax = plt.pcolormesh(t, np.arange(1,38), approx_amps, shading='gouraud')
#ax = plt.pcolormesh(t,f,Sxx2, shading='gouraud')
#plt.axis((0,10,0,600))
#ax = plt.pcolormesh(t, np.arange(1,38), target_amps, shading='gouraud')
ns = np.arange(1,38)
#plt.plot(ns,target_amps[:,156],color='blue')
plt.show()'''

#Test Precision/Recall
objects = []
with (open("Test_14.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)
pop = objects[0]
best_individual = pop[0]
best_gen = best_individual.genome
best_gen.process_notes()
best_gen.print_notes()


ttls_genome = ttls_gen = utilities.make_ttls()
(precision,recall) = utilities.calc_precision_and_recall(ttls_genome,best_gen)
print(f"precision: {precision}")
print(f"recall: {recall}")


utilities.draw_midi(ttls_genome)
plt.title("Ground Truth")
utilities.draw_midi(best_gen)
plt.title("Best Genome from GA")
plt.show()