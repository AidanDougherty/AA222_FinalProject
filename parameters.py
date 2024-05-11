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
MAX_VELOCITY = 128 #0 to 128

CROSSOVER_PROBABILITY = 0.75