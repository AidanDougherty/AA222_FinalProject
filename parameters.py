import numpy as np
from heapq import nsmallest
notes = ["E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3",
             "E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4",
             "E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5"]
note_freqs = [82.41,87.31,92.5,98.0,103.8,110.0,116.5,123.5,130.8,138.6,146.8,155.6,
              164.8,174.6,185.0,196.0,207.7,220.0,233.1,246.9,261.6,277.2,293.7,311.1,
              329.6,349.2,370.0,392.0,415.3,440.0,466.2,493.9,523.3,554.3,587.3,622.3,659.3]

#Song/Note Characteristics
SAMPLE_RATE = 44100 #kHz
MAX_SONG_TIME = 10 #Seconds in song
MAX_NOTE_TIME = 4 #max seconds for one note
MIN_NOTE_TIME = 0.02 #min seconds for one note
MAX_SAMPLES = int(SAMPLE_RATE*MAX_SONG_TIME) #total samples in song
MAX_DURATION = int(SAMPLE_RATE*MAX_NOTE_TIME) #max samples for one note
MIN_DURATION = int(SAMPLE_RATE*MIN_NOTE_TIME) #min samples for one note
MIN_START = 0 #in samples
MAX_START = MAX_SAMPLES-MIN_DURATION
MAX_VELOCITY = 128 #0 to 128

#Genetics
CROSSOVER_PROBABILITY = 0.75
MUTATION_PROBABILITY = 0.1
MAX_START_SHIFT = 0.5 #in seconds, for note mutation
MAX_VELOCITY_SHIFT = 16 #for note mutation

#Random Genome Creation
MIN_NUMBER_NOTES = 5 #for uniform genome sampling
MAX_NUMBER_NOTES = 30

#Fitness Evaluation
DOWNSAMPLE_FACTOR = 10
DOWNSAMPLE_FS = int(SAMPLE_RATE/DOWNSAMPLE_FACTOR)

FRAME_SAMPLES = 1024 #after downsampling by 10
FRAME_OVERLAP = 0.5
NUM_FRAMES = int((MAX_SAMPLES/DOWNSAMPLE_FACTOR)/(FRAME_SAMPLES*(1-FRAME_OVERLAP))) - 1
NFFT = 4*FRAME_SAMPLES
FREQ_AXIS = np.linspace(0,DOWNSAMPLE_FS/2,int(NFFT/2)) #real freq axis of NFFT point FFT of downsampled frame
NOTE_INDICES = np.array([[np.where(FREQ_AXIS==f)[0] for f in nsmallest(3, FREQ_AXIS, key=lambda x: abs(x - nf))] for nf in note_freqs]).reshape(37,3).T
#^3x37 array of 3 closest indices in FREQ_AXIS to each note

NORMALIZATION_OPT = False
MAX_RESCALE_FACTOR = 10

GENERATION_TOLERANCE = 1e4

#Population Parameters
POP_SIZE = 200
NUM_CHILDREN = 100
NUM_PARENTS = 90
NUM_MUTATE_BEST = NUM_CHILDREN - NUM_PARENTS #proportion of population that is created from mutating best individual
ELITE_SIZE = 200
NUM_GENERATIONS = 100
TOURNAMENT_SIZE = 5