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
import copy
random.seed(2)

#CHANGE THIS PATH FOR NEW SONG
#ALSO CHANGE PATH IN GENOME TO POINT TO NOTES FOLDER
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'

ideal_genome = utilities.make_ttls() #ideal genome for twinkle twinkle little star target
(population,gen_fitness,best_fit,gen_performance,best_individual_overall) = GeneticAlgorithm.run_ga(readpath,ideal_genome)
best_individual = population[0]
second = population[1]

print(f"Best Fitness: {best_fit}")
gen = copy.copy(best_individual_overall.genome)
gen.process_notes()
s = gen.synthesize()
wavfile.write('best.wav',parameters.SAMPLE_RATE,s)

with open('Test_25.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([population, gen_fitness, gen_performance,best_individual_overall], f)

plt.figure()
plt.plot(np.arange(0,len(gen_fitness)),gen_fitness)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness vs Generation")

plt.figure()
plt.plot(np.arange(0,len(gen_performance)),gen_performance)
plt.xlabel("Generation")
plt.ylabel("Performance")
plt.title("Best Performance vs Generation")

#best_individual.genome.process_notes()
#second.genome.process_notes()
utilities.draw_midi(gen)
plt.title("Best Individual Across All Generations")
#utilities.draw_midi(second.genome)
#plt.title("Second Best Individual")

ideal_genome = utilities.make_ttls()
(best_precision, best_recall) = utilities.calc_precision_and_recall(ideal_genome,gen)
print(f"precision: {best_precision}")
print(f"recall: {best_recall}")
print(f"best performance: {best_precision*best_recall}")

(f,t,Sxx) = utilities.calc_spectrogram(utilities.downsample(s))
Sxx = utilities.normalize_frames(Sxx)
plt.figure()
ax = plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.axis((0,10,0,600))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
