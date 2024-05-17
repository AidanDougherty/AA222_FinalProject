import GeneticAlgorithm
import Individual
import Genome
import utilities
import matplotlib.pyplot as plt
import numpy as np
import random
random.seed(1)
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
(best_individual,gen_fitness) = GeneticAlgorithm.run_ga(readpath)
plt.plot(np.arange(0,len(gen_fitness)),gen_fitness)
plt.show()

utilities.draw_midi(best_individual.genome)
