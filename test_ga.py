import GeneticAlgorithm
import Individual
import Genome
import utilities
import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
import parameters
import scipy.io.wavfile as wavfile
random.seed(1)
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
(population,gen_fitness,best_fit) = GeneticAlgorithm.run_ga(readpath)
best_individual = population[0]
second = population[1]
print(f"Best Fitness: {best_fit}")
s = best_individual.genome.synthesize()
wavfile.write('best.wav',parameters.SAMPLE_RATE,s)

with open('FFT_noNorm_200gen_freqpen.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([population, gen_fitness], f)

plt.figure()
plt.plot(np.arange(0,len(gen_fitness)),gen_fitness)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness vs Generation, no Normalization, FFT-based, Freq penalty")


utilities.draw_midi(best_individual.genome)
plt.title("Best Individual")
utilities.draw_midi(second.genome)
plt.title("Second Best Individual")
(f,t,Sxx) = utilities.calc_spectrogram(utilities.downsample(best_individual.genome.synthesize()))
Sxx = utilities.normalize_frames(Sxx)
plt.figure()
ax = plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.axis((0,10,0,600))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
