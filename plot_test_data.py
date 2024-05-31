import Individual
import Genome
import utilities
import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
import parameters
import scipy.io.wavfile as wavfile
import GeneticAlgorithm as ga

readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
ttls = utilities.make_ttls()
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
(f,t,Sxx) = utilities.calc_spectrogram(song)
target_Sxx = utilities.normalize_frames(Sxx)
target_amps = utilities.eval_note_amplitudes(target_Sxx)

objects = []
with (open("Test_28.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)

#Plot fitness
fitness = objects[1]
n = np.arange(0,len(fitness))
fig,ax = plt.subplots()
ax.plot(n,fitness)
ax.set_title("Fitness vs Generation")

#plot performance
performance = objects[2]
n = np.arange(0,len(performance))
fig,ax = plt.subplots()
ax.plot(n,performance)
ax.set_title("Best Performance vs Generation")
ax.set_ylim(0,1)

population = objects[0]
#best_individual = population[0]
#second = population[1]
#(best_perf,best_individual) = ga.calc_best_performance(population,ttls)
#print(best_individual.evaluate_self(target_amps))
#print(best_perf)
best_individual = objects[3]
best_individual.genome.process_notes()

#print(second.evaluate_self(target_amps))
utilities.draw_midi(best_individual.genome)
#best_individual.genome.process_notes()
#utilities.draw_midi(best_individual.genome)
(best_p,best_r) = utilities.calc_precision_and_recall(ttls,best_individual.genome)
print(f"Best precision: {best_p}")
print(f"Best recall: {best_r}")
print(f"Best performance: {best_p*best_r}")
plt.show()