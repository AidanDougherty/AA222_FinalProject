import Genome
import parameters
import numpy as np
import scipy.signal as sig
import utilities
import copy
class Individual:
    def __init__(self,genome=Genome.Genome()): #default random genome
        if(not isinstance(genome,Genome.Genome)):
            print("ERROR: genome must be of type Genome.Genome")
            return
        self.genome = genome
        self.fitness = -1
    
    def evaluate_self(self,target_note_amps):
        if(self.fitness==-1):
            phenotype = self.genome.synthesize() #downsampled already
            phenotype = utilities.downsample(phenotype)
            (f,t,Sxx) = utilities.calc_spectrogram(phenotype)
            if(parameters.NORMALIZATION_OPT):
                Sxx = utilities.normalize_frames(Sxx)
            
            #Bin frames by note frequency
            #compare to binned values in target -> fitness
            note_amps = utilities.eval_note_amplitudes(Sxx)
            #note_amps = utilities.rescale_to_target(note_amps,target_note_amps)
            target_peak_ind = np.argmax(target_note_amps,axis=0)
            note_peak_ind = np.argmax(note_amps,axis=0)
            self.fitness = np.mean(np.abs(target_note_amps-note_amps)) #+ 2e3*np.mean(np.abs(target_peak_ind-note_peak_ind)) #absolute freq frame penalty and avg relative peak freq diff pen
            #self.fitness = np.sum(np.abs(target_note_amps-Sxx))
            return self.fitness
        else:
            return self.fitness
    
    def evaluate_self_Sxx(self,target_Sxx):
        if(self.fitness==-1):
            phenotype = self.genome.synthesize() #downsampled already
            #phenotype = utilities.downsample(phenotype)
            (f,t,Sxx) = utilities.calc_spectrogram(phenotype)
            if(parameters.NORMALIZATION_OPT):
                Sxx = utilities.normalize_frames(Sxx)
            Sxx = utilities.rescale_to_target(Sxx,target_Sxx)
            #Bin frames by note frequency
            #compare to binned values in target -> fitness
            
            target_peak_ind = np.argmax(target_Sxx,axis=0)
            note_peak_ind = np.argmax(target_Sxx,axis=0)
            self.fitness = np.sum(np.abs(target_Sxx-Sxx)) #+ 1e7*np.mean(np.abs(target_peak_ind-note_peak_ind)) #absolute freq frame penalty and avg relative peak freq diff pen
            #self.fitness = np.sum(np.abs(target_note_amps-Sxx))
            return self.fitness
        else:
            return self.fitness
        
    def reproduce(self,other):
        (child_gen1,child_gen2) = self.genome.crossover(other.genome)
        child_gen1.mutate()
        child_gen2.mutate()
        return (Individual(child_gen1),Individual(child_gen2))
    
    def clone_and_mutate(self):
        clone_genome = copy.copy(self.genome)
        clone_genome.mutate()
        return Individual(clone_genome)



    