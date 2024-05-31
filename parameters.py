import numpy as np
from heapq import nsmallest
notes = ["E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3",
             "E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4",
             "E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5"]
note_freqs = [82.41,87.31,92.5,98.0,103.8,110.0,116.5,123.5,130.8,138.6,146.8,155.6,
              164.8,174.6,185.0,196.0,207.7,220.0,233.1,246.9,261.6,277.2,293.7,311.1,
              329.6,349.2,370.0,392.0,415.3,440.0,466.2,493.9,523.3,554.3,587.3,622.3,659.3]
rescale_factors = [1.16840175, 0.4660478,  0.46096584, 0.4628853,  0.479128,   1.08777462,
 1.14570161, 1.0903078,  1.15441964, 1.16508956, 2.33757729, 0.70704109,
 0.7226515,  0.72612847, 0.75000186, 0.81177717, 1.32788544, 1.33179828,
 1.3588005,  4.79582411, 1.39329951, 1.42030793, 1.4138068,  1.41491398,
 1.44565105, 4.17606239, 4.27091016, 4.36240424, 4.55635666, 4.86705832,
 5.10339702, 5.28464965, 5.20398652, 5.37344897, 5.2155399,  5.5298588,
 5.48012292]


#Song/Note Characteristics
ORIGINAL_SAMPLE_RATE = 44100
DOWNSAMPLE_FACTOR = 10
#SAMPLE_RATE = int(ORIGINAL_SAMPLE_RATE/DOWNSAMPLE_FACTOR) #kHz
SAMPLE_RATE = ORIGINAL_SAMPLE_RATE
MAX_SONG_TIME = 10 #Seconds in song
MAX_NOTE_TIME = 4 #max seconds for one note
MIN_NOTE_TIME = 0.1 #min seconds for one note
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
MAX_DURATION_CHANGE = 1.5 #x100% = maximum duration change as a proportion for mutation
#change to 1.5 for aprrox init pop

#Random Genome Creation
MIN_NUMBER_NOTES = 5 #for uniform genome sampling
MAX_NUMBER_NOTES = 30

#Fitness Evaluation
DOWNSAMPLE_FACTOR = 10
DOWNSAMPLE_FS = int(SAMPLE_RATE/DOWNSAMPLE_FACTOR)

FRAME_SAMPLES = 512 #after downsampling by 10 (4096 for ds)
FRAME_OVERLAP = 0.5 #x100 = % overlapping (0.9)
NUM_FRAMES = int(np.ceil((MAX_SAMPLES/DOWNSAMPLE_FACTOR-FRAME_SAMPLES)/(FRAME_SAMPLES*(1-FRAME_OVERLAP)))) 
NFFT = 8*FRAME_SAMPLES #freq spacing = 1 Hz, freq resolution with hanning = 8 Hz, (same as frame samples for ds)
FREQ_AXIS = np.linspace(0,DOWNSAMPLE_FS/2,int(NFFT/2)) #real freq axis of NFFT point FFT of downsampled frame
FREQ_PER_NOTE = 1
NOTE_INDICES = np.array([[np.where(FREQ_AXIS==f)[0] for f in nsmallest(FREQ_PER_NOTE, FREQ_AXIS, key=lambda x: abs(x - nf))] for nf in note_freqs]).reshape(37,FREQ_PER_NOTE).T
#^3x37 array of FREQ_PER_NOTE closest indices in FREQ_AXIS to each note

NORMALIZATION_OPT = False
MAX_NORMALIZATION_FACTOR = 10
MAX_RESCALE_FACTOR = 2 
HARMONIC_ATTEN_FACTOR = 0.1
HARMONIC_TO_PEAK_RATIO = 0.3 #ratio of harmonics to fundamental

GENERATION_TOLERANCE = .001

#Population Parameters
POP_SIZE = 200
NUM_CHILDREN = 100
NUM_PARENTS = 90
NUM_MUTATE_BEST = NUM_CHILDREN - NUM_PARENTS #proportion of population that is created from mutating best individual
ELITE_SIZE = 200
NUM_GENERATIONS = 100
TOURNAMENT_SIZE = 5

#Precision/Recall parameters
MATCH_START_TOL = int(0.5*SAMPLE_RATE)
MATCH_DUR_TOL = int(0.5*SAMPLE_RATE)


#For runnning tests:
USE_APPROX = True
USE_FREQ_PEN = True
RESCALE_OPT = True