import Genome
import Note
from scipy.io import wavfile
import numpy as np
import utilities
import random
import copy
import parameters

#Test Synthesize
'''
n1 = Note.Note(noteName='C3',startTime=int(1*parameters.SAMPLE_RATE),duration=int(0.5*parameters.SAMPLE_RATE),velocity=64)
n2 = copy.copy(n1)
n2.shift_start(n1.duration+int(0.001*parameters.SAMPLE_RATE))
gen = Genome.Genome([n1,n2])
s = gen.synthesize()
wavfile.write('test.wav',parameters.SAMPLE_RATE,s)
gen.print_notes()
'''

#Test Crossover
'''
random.seed(34)
scale_down = utilities.make_Cmaj_down()
scale_up = utilities.make_Cmaj_up()

(s1,s2) = scale_down.crossover(scale_up)
s1.print_notes()
s2.print_notes()
'''
'''
#Draw Midi Notes
scale_up = utilities.make_Cmaj_up()
utilities.draw_midi(scale_up)
'''