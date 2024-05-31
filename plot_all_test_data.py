import Individual
import Genome
import utilities
import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
import parameters
import scipy.io.wavfile as wavfile

objects = []
with (open("Test_29.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)
pop1 = objects[0]
fit1 = objects[1]
perf1 = objects[2]

objects = []
with (open("Test_30.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)
pop2 = objects[0]
fit2 = objects[1]
perf2 = objects[2]

objects = []
with (open("Test_28.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)
pop3 = objects[0]
fit3 = objects[1]
perf3 = objects[2]
best_indiv3 = objects[3]

objects = []
with (open("Test_27.pkl", "rb")) as openfile:
    objects = pickle.load(openfile)
pop4 = objects[0]
fit4 = objects[1]
perf4 = objects[2]

fig,ax = plt.subplots()
n = np.arange(0,len(perf1))
ax.plot(perf1,label="Random")
ax.plot(perf2,label="Random + Freq Penalty")
ax.plot(perf3,label="Estimation")
ax.plot(perf4,label="Estimation + Freq Penalty")
ax.legend(loc="upper left")
ax.set_title("Performance vs Generation")
#plt.show()

ttls = utilities.make_ttls()
readpath = 'C:/Users/dough/OneDrive/Documents/AA222_FinalProject/TTLS.wav'
song = utilities.process_wav(readpath)
song = utilities.downsample(song)
(f,t,Sxx) = utilities.calc_spectrogram(song)
target_Sxx = utilities.normalize_frames(Sxx)
target_amps = utilities.eval_note_amplitudes(target_Sxx)
approx_genome = utilities.fit_notes(target_amps)
(init_prec,init_recall) = utilities.calc_precision_and_recall(ttls,approx_genome)
init_perf = init_prec*init_recall
print(f"Estimation Performance: {init_perf}")
best_gen = best_indiv3.genome
best_gen.process_notes()
best_gen.print_notes()
(best_prec,best_recall) = utilities.calc_precision_and_recall(ttls,best_gen)
best_perf = best_prec*best_recall
print(f"Final Performance: {best_perf}")

utilities.draw_midi(approx_genome)
plt.title("Estimation MIDI")
utilities.draw_midi(best_gen)
plt.title("Best Genome from GA")
plt.show()