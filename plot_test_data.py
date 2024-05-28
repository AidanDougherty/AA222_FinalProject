import Individual
import Genome
import utilities
import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
import parameters
import scipy.io.wavfile as wavfile

readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
(f,t,Sxx) = utilities.calc_spectrogram(song)
target_Sxx = utilities.normalize_frames(Sxx)
target_amps = utilities.eval_note_amplitudes(target_Sxx)

objects = []
with (open("Test_11.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)

#Plot fitness
fitness = objects[1]
n = np.arange(1,len(fitness)+1)
fig,ax = plt.subplots()
ax.plot(n,fitness)
ax.set_title("Fitness vs Generation")

population = objects[0]
best_individual = population[0]
second = population[1]
print(best_individual.evaluate_self(target_amps))
print(second.evaluate_self(target_amps))
utilities.draw_midi(best_individual.genome)
best_individual.genome.remove_overlap_notes()
utilities.draw_midi(best_individual.genome)

plt.show()