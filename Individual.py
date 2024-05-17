import Genome
import parameters
import numpy as np
import scipy.signal as sig
import utilities
class Individual:
    def __init__(self,genome=Genome.Genome()): #default random genome
        if(not isinstance(genome,Genome.Genome)):
            print("ERROR: genome must be of type Genome.Genome")
            return
        self.genome = genome
        self.fitness = -1
    
    def evaluate_self(self,target):
        if(not self.fitness==-1):
            phenotype = self.genome.synthesize()
            phenotype = utilities.downsample(phenotype)
            (f,t,Sxx) = utilities.calc_spectrogram(phenotype)
            if(parameters.NORMALIZATION_OPT):
                Sxx = utilities.normalize_spec_frames(Sxx)

            #Bin frames by note frequency
            #compare to binned values in target -> fitness
            
        else:
            return self.fitness

    