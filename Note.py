import random
import parameters
class Note:
    notes = parameters.notes
    SAMPLE_RATE = parameters.SAMPLE_RATE #kHz
    MAX_SONG_TIME = parameters.MAX_SONG_TIME #Seconds in song
    MAX_NOTE_TIME = parameters.MAX_NOTE_TIME #max seconds for one note
    MIN_NOTE_TIME = parameters.MIN_NOTE_TIME #min seconds for one note
    MAX_SAMPLES = parameters.MAX_SAMPLES #total samples in song
    MAX_DURATION = parameters.MAX_DURATION #max samples for one note
    MIN_DURATION = parameters.MIN_DURATION #min samples for one note
    MAX_START = parameters.MAX_START
    MIN_START = parameters.MIN_START #in samples
    MAX_VELOCITY = parameters.MAX_VELOCITY
    def __init__(self,noteName=None,startTime=None,duration=None,velocity=None):
        if(all(x==None for x in [noteName,startTime,duration,velocity])): #default constructor
            self.set_rand_param()
            return
        else:
            if(noteName in Note.notes):
                self.noteName = noteName
            else:
                raise Exception("invalid noteName, choose between E2 and E5")
            #TODO:Implement Checks on min/max range
            self.startTime = int(startTime) #in samples, int
            self.duration = int(duration) #in samples, int
            self.velocity = int(velocity) #int from 0 to 128

    #RANDOM NOTE GENERATION (UNIFORM DISTRIBUTION)
    def set_rand_param(self):
        self.noteName = random.choice(Note.notes)
        self.startTime = int(random.random()*(Note.MAX_START-Note.MIN_START))+Note.MIN_START
        dur = int(random.random()*(Note.MAX_DURATION-Note.MIN_DURATION))+Note.MIN_DURATION
        if(self.startTime+dur<=Note.MAX_SAMPLES): #check note doesn't go over song length
            self.duration = dur
        else:
            self.duration = int(Note.MAX_SAMPLES-self.startTime)
        self.velocity = int(random.random()*Note.MAX_VELOCITY)

    #directionIsUp = boolean, True = shift up
    def shift_octave(self,directionIsUp):
        i = Note.notes.index(self.noteName)
        L = len(Note.notes)
        if(directionIsUp):
            self.noteName = Note.notes[(i+12)%L]
        else:
            self.noteName = Note.notes[(i-12)%L]
    
    def shift_semitone(self,directionIsUp):
        i = Note.notes.index(self.noteName)
        L = len(Note.notes)
        if(directionIsUp):
            self.noteName = Note.notes[(i+1)%L]
        else:
            self.noteName = Note.notes[(i-1)%L]

    #0.5<proportion<1.5, float, scales duration 50-150%
    def change_duration(self,proportion):
        new_duration = int(self.duration*proportion)
        if(new_duration<=Note.MAX_DURATION and new_duration>=Note.MIN_DURATION): #valid duration
            if(new_duration+self.startTime<=Note.MAX_SAMPLES): #doesn't go over song length
                self.duration = new_duration
            else:
                self.duration = Note.MAX_SAMPLES - self.startTime #if goes over, play note til end
        elif(new_duration>Note.MAX_DURATION):
            self.duration = Note.MAX_DURATION #upper bound on duration
        else:
            self.duration = Note.MIN_DURATION #lower bound
            
    #sampleShift = integer, shift start time by sampleShift samples
    def shift_start(self,sampleShift):
        new_startTime = self.startTime+sampleShift
        if(new_startTime<=Note.MAX_START and new_startTime>=Note.MIN_START):
            if(new_startTime+self.duration<=Note.MAX_SAMPLES):
                self.startTime = new_startTime
            else:
                self.startTime = Note.MAX_SAMPLES-self.duration
        elif(new_startTime<Note.MIN_START):
            self.startTime = Note.MIN_START
        else:
            self.startTime = Note.MAX_START
    #shift velocity by vel_change amount, if sets to 0 or below, return 0 flag indicating to delete note
    def shift_velocity(self,vel_change):
        new_vel =self.velocity+vel_change
        if(new_vel<Note.MAX_VELOCITY and new_vel>0):
            self.velocity = new_vel
            return 1
        elif(new_vel>=Note.MAX_VELOCITY):
            self.velocity = Note.MAX_VELOCITY
            return 1
        else:
            return 0
        

    

