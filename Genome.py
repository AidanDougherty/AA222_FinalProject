import random
import Note
from scipy.io import wavfile
import numpy as np
class Genome:
    readpath = 'c:/Users/dough/OneDrive/Documents/AA222_FinalProject/Notes/'
    #TODO: IMPLEMENT RANDOM NOTE SEQUENCE GENERATION (UNIFORM)
    def __init__(self,noteList):
        if any(not isinstance(x, Note.Note) for x in noteList):
            print("ERROR: noteList must contain only objects of type NOTE")
            return
        else:
            sorted_noteList = sorted(noteList, key=lambda x: x.startTime, reverse=False)
        self.noteList = sorted_noteList #list of notes, sorted by start time
    

    def crossover(self,partner):
        #TODO: IMPLEMENT POINT CUT RECOMBINATION, RETURN NEW GENOME
        pass

    #return int16 array of samples at 44.1kHz using .wav files in Notes
    def synthesize(self):
        n = Note.Note()
        song = np.zeros(n.MAX_SAMPLES+1)
        for n in self.noteList:
            samplerate, data = wavfile.read(Genome.readpath+n.noteName+'.wav') #velocity = 64
            note_data = data[:n.duration] #set duration, maybe add tapering
            note_data = (note_data*(n.velocity/64)) #set velocity
            song[n.startTime:n.startTime+n.duration]+=note_data
        #add rescaling?
        return song.astype(np.int16)
        