import random
import Note
import parameters
import copy
from scipy.io import wavfile
import numpy as np
class Genome:
    readpath = 'c:/Users/dough/OneDrive/Documents/AA222_FinalProject/Notes/'
    #TODO: IMPLEMENT RANDOM NOTE SEQUENCE GENERATION (UNIFORM)? -> initial population from note estimation on song, not random
    def __init__(self,noteList):
        if any(not isinstance(x, Note.Note) for x in noteList):
            print("ERROR: noteList must contain only objects of type NOTE")
            return
        else:
            sorted_noteList = sorted(noteList, key=lambda x: x.startTime, reverse=False) #sort by start time
        #implement max number of notes?
        self.noteList = sorted_noteList #list of notes, sorted by start time
    
    def crossover(self,partner):
        #TODO: IMPLEMENT POINT CUT RECOMBINATION, RETURN 2 NEW GENOMES
        if (random.random()>=parameters.CROSSOVER_PROBABILITY): #25% chance of no crossover, children are identical to parents
            return [copy.copy(self), copy.copy(partner)]
        #otherwise do crossover
        cross_time = int(random.random()*parameters.MAX_SAMPLES)
        self_genomes = self.split_genome(cross_time)
        partner_genomes = partner.split_genome(cross_time)
        return [Genome.Genome([self_genomes[0]+partner_genomes[1]]), Genome.Genome([self_genomes[1]+partner_genomes[0]])]

    #Split one genome into 2 at crosstime, returns two genomes
    def split_genome(self,cross_time):
        #find which notes are playing at cross time
        notelist_A = [] #before cut
        notelist_B = [] #after
        notes_playing_ind = [] #indices of notes that need to be cut in half
        for i in range(0,len(self.noteList)): #find notes needing to be split
            st = self.noteList[i].startTime
            d = self.noteList[i].duration
            if(cross_time>st and cross_time<st+d):
                notes_playing_ind.append(i)
        for n in self.noteList:
            if(n.startTime<cross_time and not self.noteList.index(n) in notes_playing_ind ): #note is before cross time and not playing
                notelist_A.append(copy.copy(n))
            elif(n.startTime>=cross_time):
                notelist_B.append(copy.copy(n))
            else: #note is currently playing
                n_A = Note.Note(n.noteName,n.startTime,cross_time-n.startTime,n.velocity)
                notelist_A.append(n_A)
                n_B = Note.Note(n.noteName,cross_time,n.startTime+n.duration-cross_time,n.velocity)
                notelist_B.append(n_B)
        return [Genome.Genome(notelist_A), Genome.Genome(notelist_B)]

    #return int16 array of samples at 44.1kHz using .wav files in Notes
    def synthesize(self):
        song = np.zeros(parameters.MAX_SAMPLES+1)
        for n in self.noteList:
            samplerate, data = wavfile.read(Genome.readpath+n.noteName+'.wav') #velocity = 64
            note_data = data[:n.duration] #set duration, maybe add tapering
            note_data = (note_data*(n.velocity/(parameters.MAX_VELOCITY/2))) #set velocity, add averaging?
            song[n.startTime:n.startTime+n.duration]+=note_data
        #add rescaling? -> normalize frames in eval
        return song.astype(np.int16)
        