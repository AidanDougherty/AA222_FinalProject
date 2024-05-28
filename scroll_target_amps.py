import Genome
import Note
import Individual
from scipy.io import wavfile
import numpy as np
import utilities
import random
import copy
import parameters
import matplotlib.pyplot as plt
import sys
import pickle

n=0
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
(f,t,Sxx) = utilities.calc_spectrogram(song)
target_Sxx = utilities.normalize_frames(Sxx)
target_amps = utilities.eval_note_amplitudes(target_Sxx)
ta_max = np.max(target_amps)
#target_amps = target_amps/ta_max

'''fit_notes = utilities.fit_notes(target_amps)
fit_syn = fit_notes.synthesize() #downsampled already
fit_syn = utilities.downsample(fit_syn)
(f,t,Sxx3) = utilities.calc_spectrogram(fit_syn)
fit_amps = utilities.eval_note_amplitudes(Sxx3)'''

ttls = utilities.make_ttls()
ttls_syn = ttls.synthesize() #downsampled already
ttls_syn = utilities.downsample(ttls_syn)
(f,t,Sxx3) = utilities.calc_spectrogram(ttls_syn)
ttls_amps = utilities.eval_note_amplitudes(Sxx3)
ttls_amps = utilities.rescale_to_target(ttls_amps,target_amps)
#ttls_amps = ttls_amps/ta_max

objects = []
with (open("Test_10.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)
pop = objects[0]
best_individual = pop[0]
best_gen = best_individual.genome
phenotype = best_gen.synthesize() #downsampled already
phenotype = utilities.downsample(phenotype)
(f,t,Sxx2) = utilities.calc_spectrogram(phenotype)
best_notes = utilities.eval_note_amplitudes(Sxx2)
best_notes = utilities.rescale_to_target(best_notes,target_amps)
#best_notes = best_notes/ta_max

def on_press(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'x':
        ax.cla()
        global n
        n+=1
        ax.plot(ns,target_amps[:,n],color='blue')
        ax.plot(ns,best_notes[:,n],color='red')
        #ax.plot(ns,fit_amps[:,n],color='green')
        ax.plot(ns,ttls_amps[:,n],color='green')
        ax.set_title(f"Frame {n}, t={t[n]:2.3}")
        ax.set_ylim([0, 1e6])
        plt.show()


# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()

fig.canvas.mpl_connect('key_press_event', on_press)

ns = np.arange(1,38)
ax.plot(ns,target_amps[:,n],color='blue')
ax.plot(ns,best_notes[:,n],color='red')
#ax.plot(ns,fit_amps[:,n],color='green')
ax.plot(ns,ttls_amps[:,n],color='green')
ax.set_ylim([0, 1e6])



#fig2,ax2 = plt.subplots()
#ax2.pcolormesh(t, np.arange(1,38), target_amps, shading='gouraud')


plt.show()