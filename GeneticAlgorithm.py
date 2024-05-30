import parameters
import utilities
import Individual
import copy
import random
import numpy as np
def run_ga(readpath,ideal_genome): #path to 44.1kHz, 10s song
    
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
    if(parameters.USE_APPROX): #use approximation as starting basis
        population = [Individual.Individual(approx_genome)] #list of Individuals
        for i in range(0,parameters.POP_SIZE-1):
            mutated_gen = copy.copy(approx_genome)
            mutated_gen.mutate(forced=True)
            population.append(Individual.Individual(mutated_gen))
    else: #completely random population
        population = []
        for i in range(0,parameters.POP_SIZE):
            population.append(Individual.Individual())
    
    gen_fitness = np.zeros(parameters.NUM_GENERATIONS+1) #array for storing average fitness of each generation
    gen_performance = np.zeros(parameters.NUM_GENERATIONS+1)
    best_perf_overall = 0 
    for ngen in range(0,parameters.NUM_GENERATIONS):
        print(f"Generation #: {ngen}")
        #tournament select + reproduce -> 90 new individuals
        #clone+mutate the best -> 10 new individual
        population = sorted(population, key=lambda x: x.evaluate_self(target_note_amps), reverse=False)[:parameters.POP_SIZE] #sort by fitness, low (good) to high (bad), take best 200
        best_individual = population[0]
        gen_fitness[ngen] = calc_average_fitness(population,target_note_amps)
        #gen_performance[ngen] = calc_average_performance(population,ideal_genome)
        (best_perf,best_perf_ind) = calc_best_performance(population,ideal_genome)
        gen_performance[ngen] = best_perf
        if(best_perf>best_perf_overall):
            best_perf_overall=best_perf
            best_individual_overall = best_perf_ind
        print(f"Current Fitness: {gen_fitness[ngen]}")
        print(f"Current Performance: {gen_performance[ngen]}")
        if(ngen>0):
            if(np.abs(gen_fitness[ngen-1]-gen_fitness[ngen])<=parameters.GENERATION_TOLERANCE):
                break
        
        parents = tournament_select(population,parameters.TOURNAMENT_SIZE,parameters.NUM_PARENTS,target_note_amps) #tournament selection and reproduction
        parentsA = parents[:len(parents)//2]
        parentsB = parents[len(parents)//2:]
        for i in range(0,len(parentsA)): #crossover
            (child1,child2) = parentsA[i].reproduce(parentsB[i])
            population.append(child1)
            population.append(child2)
        
        for i in range(0,parameters.NUM_MUTATE_BEST):
            population.append(best_individual.clone_and_mutate())
    
    population = sorted(population, key=lambda x: x.evaluate_self(target_note_amps), reverse=False)[:parameters.POP_SIZE]
    gen_fitness = np.trim_zeros(gen_fitness)
    gen_performance = np.trim_zeros(gen_performance)
    best_fitness = population[0].evaluate_self(target_note_amps)
    return (population,gen_fitness,best_fitness,gen_performance,best_individual_overall)

def calc_average_fitness(pop,target_note_amps):
    total = 0
    for x in pop:
        total+=x.evaluate_self(target_note_amps)
    return total/len(pop)

def calc_average_performance(pop,ideal_genome):
    total = 0
    for x in pop:
        gen = copy.copy(x.genome)
        gen.process_notes()
        (precision,recall) = utilities.calc_precision_and_recall(ideal_genome,gen)
        total+=precision*recall
    return total/len(pop)

def calc_best_performance(pop,ideal_genome):
    best = 0
    
    for x in pop:
        gen = copy.copy(x.genome)
        gen.process_notes()
        (precision,recall) = utilities.calc_precision_and_recall(ideal_genome,gen)
        perf = precision*recall
        if(perf>best):
            best = perf
            best_ind = x
    
    return (best,best_ind)

def tournament_select(pop, tournament_size,num_winners,target_note_amps):
    population = copy.copy(pop)
    winners = []
    for i in range(0,num_winners):
        competitors = random.sample(population,tournament_size) #get 5 competitors at random
        best = sorted(competitors, key=lambda x: x.evaluate_self(target_note_amps), reverse=False)[0]
        winners.append(best)
        population.remove(best)
    return winners

