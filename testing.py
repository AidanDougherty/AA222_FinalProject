import Genome
import Note
from scipy.io import wavfile
import numpy as np

n1 = Note.Note()
n2 = Note.Note()
gen = Genome.Genome([n1,n2])
s = gen.synthesize()
wavfile.write('test.wav',n1.SAMPLE_RATE,s)