import random
class Note:
    notes = ["E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3",
             "E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4",
             "E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5"]
    SAMPLE_RATE = 44100 #kHz
    MAX_SONG_TIME = 10 #Seconds in song
    MAX_NOTE_TIME = 4 #max seconds for one note
    MIN_NOTE_TIME = 0.02 #min seconds for one note
    MAX_SAMPLES = int(SAMPLE_RATE*MAX_SONG_TIME) #total samples in song
    MAX_DURATION = int(SAMPLE_RATE*MAX_NOTE_TIME) #max samples for one note
    MIN_DURATION = int(SAMPLE_RATE*MIN_NOTE_TIME) #min samples for one note
    MIN_START = 0 #in samples
    MAX_VELOCITY = 128
    def __init__(self,noteName=None,startTime=None,duration=None,velocity=None):
        if(all(x==None for x in [noteName,startTime,duration,velocity])):
            self.set_rand_param()
            return
        else:
            if(noteName in Note.notes):
                self.noteName = noteName
            else:
                raise Exception("invalid noteName, choose between E2 and E5")
            self.startTime = startTime #in samples, int
            self.duration = duration #in samples, int
            self.velocity = velocity #int from 0 to 128

    #RANDOM NOTE GENERATION (UNIFORM DISTRIBUTION)
    def set_rand_param(self):
        self.noteName = random.choice(Note.notes)
        self.startTime = int(random.random()*Note.MAX_SAMPLES)
        dur = int(random.random()*Note.MAX_DURATION)
        if(self.startTime+dur<=Note.MAX_SAMPLES):
            self.duration = dur
        else:
            self.duration = Note.MAX_SAMPLES-self.startTime
        self.velocity = int(random.random()*Note.MAX_VELOCITY)

    #directionIsUp = boolean, True = shift up
    def shift_octave(self,directionIsUp):
        i = Note.notes.index(self.noteName)
        L = len(Note.notes)
        if(directionIsUp):
            self.noteName = Note.notes[(i+13)%L]
        else:
            self.noteName = Note.notes[(i-13)%L]
    
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
                self.duration = proportion*self.duration
            else:
                self.duration = Note.MAX_SAMPLES - self.startTime #if goes over, play note til end
        elif(new_duration>Note.MAX_DURATION):
            self.duration = Note.MAX_DURATION #upper bound on duration
        else:
            self.duration = Note.MIN_DURATION #lower bound
            
    #sampleShift = integer, shift start time by sampleShift samples
    def shift_start(self,sampleShift):
        new_startTime = self.startTime+sampleShift
        if(new_startTime+self.duration<=Note.MAX_SAMPLES and new_startTime>=Note.MIN_START):
            self.startTime = new_startTime
        elif(new_startTime+self.duration>Note.MAX_SAMPLES):
            self.startTime = Note.MAX_SAMPLES-self.duration
        else:
            self.startTime = Note.MIN_START

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
        

