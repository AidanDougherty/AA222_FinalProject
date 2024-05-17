import GeneticAlgorithm
import Individual
import Genome
import utilities
import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
random.seed(1)
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
(best_individual,gen_fitness) = GeneticAlgorithm.run_ga(readpath)

with open('FFT_noNorm_100gen.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([best_individual, gen_fitness], f)

plt.plot(np.arange(0,len(gen_fitness)),gen_fitness)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness vs Generation, no Normalization, FFT-based")
plt.show()

utilities.draw_midi(best_individual.genome)
(f,t,Sxx) = utilities.calc_spectrogram(best_individual.genome.synthesize())
ax = plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.axis((0,10,0,600))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
