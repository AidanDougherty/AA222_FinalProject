import Genome
import parameters
class Individual:
    def __init__(self,genome):
        self.genome = genome
        self.eval = -1
    
    def evaluate_self(self):
        if(not self.eval==-1):
            #IMPLEMENT EVALUATION
            pass
        else:
            return self.eval