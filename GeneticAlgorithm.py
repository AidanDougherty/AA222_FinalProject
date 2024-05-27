import parameters
import utilities
import Individual
import copy
import random
import numpy as np
def run_ga(readpath): #path to 44.1kHz, 10s song
    song = utilities.process_wav(readpath)
    song = utilities.downsample(song)
    (f,t,Sxx) = utilities.calc_spectrogram(song)
    #if(parameters.NORMALIZATION_OPT):
        #Sxx = utilities.normalize_frames(Sxx)
    Sxx = utilities.normalize_frames(Sxx)
    #Sxx = utilities.attenuate_harmonics(Sxx)
    target_note_amps = utilities.eval_note_amplitudes(Sxx) #spectrogram of note amplitudes
    approx_genome = utilities.fit_notes(target_note_amps)

    #Make Initial Population
    population = [Individual.Individual(approx_genome)] #list of Individuals
    for i in range(0,parameters.POP_SIZE-1):
        mutated_gen = copy.copy(approx_genome)
        mutated_gen.mutate(forced=True)
        population.append(Individual.Individual(mutated_gen))
    
    gen_fitness = np.zeros(parameters.NUM_GENERATIONS+1) #array for storing average fitness of each generation
    
    for ngen in range(0,parameters.NUM_GENERATIONS):
        print(f"Generation #: {ngen}")
        #tournament select + reproduce -> 90 new individuals
        #clone+mutate the best -> 10 new individual
        population = sorted(population, key=lambda x: x.evaluate_self(target_note_amps), reverse=False)[:parameters.POP_SIZE] #sort by fitness, low (good) to high (bad), take best 200
        best_individual = population[0]
        gen_fitness[ngen] = calc_average_fitness(population,target_note_amps)
        print(f"Current Fitness: {gen_fitness[ngen]}")
        if(ngen>0):
            if(np.abs(gen_fitness[ngen-1]-gen_fitness[ngen])<=parameters.GENERATION_TOLERANCE):
                break
        
        parents = tournament_select(population,parameters.TOURNAMENT_SIZE,parameters.NUM_PARENTS,target_note_amps)
        parentsA = parents[:len(parents)//2]
        parentsB = parents[len(parents)//2:]
        for i in range(0,len(parentsA)):
            (child1,child2) = parentsA[i].reproduce(parentsB[i])
            population.append(child1)
            population.append(child2)
        
        for i in range(0,parameters.NUM_MUTATE_BEST):
            population.append(best_individual.clone_and_mutate())
    
    population = sorted(population, key=lambda x: x.evaluate_self(target_note_amps), reverse=False)[:parameters.POP_SIZE]
    gen_fitness = np.trim_zeros(gen_fitness)
    best_fitness = population[0].evaluate_self(target_note_amps)
    return (population,gen_fitness,best_fitness)

def calc_average_fitness(pop,target_note_amps):
    total = 0
    for x in pop:
        total+=x.evaluate_self(target_note_amps)
    return total/len(pop)

def tournament_select(pop, tournament_size,num_winners,target_note_amps):
    population = copy.copy(pop)
    winners = []
    for i in range(0,num_winners):
        competitors = random.sample(population,tournament_size) #get 5 competitors at random
        best = sorted(competitors, key=lambda x: x.evaluate_self(target_note_amps), reverse=False)[0]
        winners.append(best)
        population.remove(best)
    return winners

