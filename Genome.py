import random
import Note
import parameters
import copy
from scipy.io import wavfile
import numpy as np
import scipy.signal as sig
class Genome:
    readpath = 'c:/Users/dough/OneDrive/Documents/AA222_FinalProject/Notes/'
    def __init__(self,noteList=None):
        if(noteList==None): #uniform random generation of notes, number of notes specified by parameters
            noteList = []
            num_notes = int((parameters.MAX_NUMBER_NOTES - parameters.MIN_NUMBER_NOTES)*random.random())+parameters.MIN_NUMBER_NOTES
            for i in range(0,num_notes):
                noteList.append(Note.Note())
            self.noteList = noteList
            self.remove_small_notes()
            self.sort() #sort by start time
        elif any(not isinstance(x, Note.Note) for x in noteList):
            print("ERROR: noteList must contain only objects of type NOTE")
            return
        else:
            self.noteList = noteList #list of notes
            self.sort() #sort by start time
            #implement max number of notes?
    
    def __add__(self,other):
        return Genome(self.noteList + other.noteList)
    
    #return tuple of genomes: 2 children with crossed genomes
    def crossover(self,partner):
        if(random.random()>parameters.CROSSOVER_PROBABILITY):
            return(copy.copy(self),copy.copy(partner))
        else:
            cross_time = int(random.random()*parameters.MAX_SAMPLES)
            self_genomes = self.split_genome(cross_time)
            partner_genomes = partner.split_genome(cross_time)
            return (self_genomes[0]+partner_genomes[1], self_genomes[1]+partner_genomes[0])

    #Split one genome into 2 at crosstime, returns two genomes in list
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
        return [Genome(notelist_A), Genome(notelist_B)]

    def mutate(self,forced=None):
        if(not self.noteList): #do not mutate if notelist is empty
            return
        if(forced==True or random.random()<=parameters.MUTATION_PROBABILITY): #10% chance to mutate one note or whole genome
            n = random.choice(self.noteList)
            self.noteList.remove(n)
            p = random.randint(1,9) #no duration mutation for all notes
            #print(p)
            if p==1: #Note frequency change, +/- octave or half step
                q = random.random()
                if(q<0.25):
                    n.shift_octave(directionIsUp=True)
                elif(q<0.5):
                    n.shift_octave(directionIsUp=False)
                elif(q<0.75):
                    n.shift_semitone(directionIsUp=True)
                else:
                    n.shift_semitone(directionIsUp=False)
                self.noteList.append(n)
            elif p==2: #shift start time
                startShift = int((2*random.random()-1)*parameters.MAX_START_SHIFT*parameters.SAMPLE_RATE)
                n.shift_start(startShift)
                self.noteList.append(n)
            elif p==3: #change duration 50% to 200%, evenly weight pdf to 50% grow or shrink?
                prop = (parameters.MAX_DURATION_CHANGE-0.5)*random.random() + 0.5
                n.change_duration(prop)
                if(not n.duration<=parameters.MIN_DURATION): #if note becomes too small, delete
                    self.noteList.append(n)
            elif p==4:  #change velocity within +/- 16
                velShift = int((2*random.random()-1)*parameters.MAX_VELOCITY_SHIFT)
                n.shift_velocity(velShift)
                if(not n.velocity == 0): #if note becomes too quiet, delete
                    self.noteList.append(n)
            elif p==5: #even split with silence equal to half note duration
                d = n.duration
                n.change_duration(0.5)
                n_copy = copy.copy(n) #split note in two
                n_copy.shift_start(d)
                self.noteList.append(n)
                self.noteList.append(n_copy)
            elif p==6: #remove note
                pass #simply don't add back to notelist
            elif p==7: #add new note - random 
                self.noteList.append(n)
                #if(random.random()<0.5):
                    #n1 = copy.copy(n)
                #else:
                n1 = Note.Note()
                self.noteList.append(n1)
            elif p==8: #change all note velocities
                self.noteList.append(n)
                v_shift = random.randint(-4,5)
                for n_s in self.noteList:
                    n_s.shift_velocity(v_shift)
            elif p==9: #change all durations
                self.noteList.append(n)
                dur_prop = (parameters.MAX_DURATION_CHANGE-0.5)*random.random() + 0.5
                for n_s in self.noteList:
                    n_s.change_duration(dur_prop)
        
        #self.remove_overlap_notes() #remove overlapping notes
        self.remove_small_notes() #get rid of any lingering small notes
        self.sort() #sort self for convenience
        
        
    #
    '''def remove_overlap_notes(self):
        self.sort()
        new_noteList = copy.copy(self.noteList)
        L = len(self.noteList)
        for i in np.arange(0,L): #iterate over each note and check if is inside other note (of same freq) or starts before note other ends
            n = self.noteList[i]
            start = n.startTime
            end = n.startTime+n.duration
            for j in np.delete(np.arange(0,L),i): #iterate over all j != i
                n2 = self.noteList[j]
                if(n.noteName==n2.noteName):
                    full_overlap = start>=n2.startTime and end<=n2.startTime+n2.duration
                    left_side_overlap = start>=n2.startTime and start<=n2.startTime+n2.duration and n2.startTime+n2.duration<end
                    if(full_overlap): #if fully inside other note, remove
                        if(n in new_noteList):
                            new_noteList.remove(n)
                    elif(left_side_overlap): #if start before other ends, make 2 notes
                        if(n in new_noteList):
                            new_noteList.remove(n)
                            new_n = copy.copy(n)
                            new_start = n2.startTime+n2.duration#+parameters.MIN_DURATION
                            new_dur = max(0,end-new_start)
                            new_n.change_duration(new_dur/new_n.duration)
                            new_n.shift_start(new_start-new_n.startTime)
                            new_noteList.append(new_n)
                            #new_noteList.remove(n2)
                            #n2.duration = start - n2.startTime - parameters.MIN_DURATION#int(0.2*parameters.SAMPLE_RATE) #separate w small gap
                            #if(n2.duration>0):
                                #new_noteList.append(n2)
                            #else:
                                #print(n2.duration)
        self.noteList = new_noteList
        self.sort()
        self.remove_small_notes()'''
    
    def process_notes(self):
        self.remove_small_notes()
        for i in range(0,10):
            self.remove_overlap_notes()
        self.remove_small_notes()
        for i in range(0,10):
            self.combine_adjacent_notes()
        self.remove_small_notes()
        self.sort()

    def combine_adjacent_notes(self):
        self.sort()
        new_noteList = copy.copy(self.noteList)
        L = len(self.noteList)
        for i in np.arange(0,L): #iterate over each note and check if is inside other note (of same freq) or starts before note other ends
            n = self.noteList[i]
            start = n.startTime
            end = n.startTime+n.duration
            for j in np.arange(i,L): #iterate over all j > i
                n2 = self.noteList[j]
                if(n.noteName==n2.noteName and np.abs(end-n2.startTime)<0.05*parameters.SAMPLE_RATE):
                    if(n in new_noteList and n2 in new_noteList):
                        new_noteList.remove(n)
                        new_noteList.remove(n2)
                        n3 = copy.copy(n)
                        new_dur = n2.startTime+n2.duration-start
                        n3.change_duration(new_dur/n3.duration)
                        new_noteList.append(n3)
        self.noteList = new_noteList
                    
    def remove_overlap_notes(self):
        self.sort()
        for note in parameters.notes:
            sublist=[]
            notes_to_remove=[]
            for n in self.noteList:
                if(n.noteName==note):
                    sublist.append(n)
                if(len(sublist)>0):
                    notes_to_remove = Genome.minRemovels(sublist)
            for n in notes_to_remove:
                self.noteList.remove(n)
        
    
    def minRemovels(sub_noteList):
        sub_noteList = sorted(sub_noteList, key=lambda x: x.startTime, reverse=False)
        size = len(sub_noteList)
        notes_to_remove = []
        end = sub_noteList[0].startTime + sub_noteList[0].duration
        for i in range(1,size):
            if(sub_noteList[i].startTime<end): #overlap detected
                notes_to_remove.append(sub_noteList[i])
                end = min(sub_noteList[i].startTime+sub_noteList[i].duration,end)
            else:
                end = sub_noteList[i].startTime+sub_noteList[i].duration
        
        return notes_to_remove

    def remove_small_notes(self):
        new_noteList = []
        for n in self.noteList:
            if(n.duration>parameters.MIN_DURATION and n.velocity>0):
                new_noteList.append(n)
                
        self.noteList = new_noteList
    
    def sort(self):
        self.noteList = sorted(self.noteList, key=lambda x: x.startTime, reverse=False)
    
    #return int16 array of samples at 44.1kHz using .wav files in Notes
    def synthesize(self):
        song = np.zeros(parameters.MAX_SAMPLES+1)
        
        for n in self.noteList:
            samplerate, data = wavfile.read(Genome.readpath+n.noteName+'.wav') #velocity = 64
            #print(n.noteName+" "+f"{n.duration}")
            note_data = data[:n.duration] #set duration
            note_data = note_data*parameters.rescale_factors[parameters.notes.index(n.noteName)] #account for fundamental freq rescaling
            taper_prop = 0.1
            taper_width = int(np.floor(taper_prop*(n.duration)))
            w = np.arange(n.duration-taper_width,n.duration)
            w = 0.5 * (1 + np.cos(np.pi * (-2.0/taper_prop + 1 + 2.0*w/taper_prop/(n.duration)))) #tapered cosine 
            note_data = (note_data*(n.velocity/(parameters.MAX_VELOCITY/2))) #set velocity, add averaging?
            try:
                note_data[-len(w):]=np.multiply(note_data[-len(w):],w) #taper ending
            except ValueError:
                print(f"note duration: {n.duration}")
                print(f"note start time: {n.startTime}")
                print(f"Length of w: {len(w)}")
                self.print_notes()
                raise ValueError("error still occurred")
            
            try:
                song[n.startTime:n.startTime+n.duration]+=note_data
            except ValueError:
                print(f"note duration: {n.duration}")
                print(f"note start time: {n.startTime}")
                print(f"Length of w: {len(w)}")
                self.print_notes()
                raise ValueError("error still occurred")
            
        #add rescaling? -> normalize frames in eval
        return song.astype(np.int16)
    
    def print_notes(self):
        notes = [n.noteName for n in self.noteList]
        print(f"Notes: {notes}")
        startTimes = [round(n.startTime/parameters.SAMPLE_RATE,5) for n in self.noteList]
        print(f"Start Times (s): {startTimes}")
        durations = [round(n.duration/parameters.SAMPLE_RATE,5) for n in self.noteList]
        print(f"Durations: {durations}")
        pass
        