import Genome
import Note
import Individual
import parameters
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
from scipy.io import wavfile
import scipy.signal as sig

def make_Genome_from_notes(noteNames): #evenly spaced notes from list of note names
    samp_per_note = int(parameters.MAX_SAMPLES/len(noteNames))
    noteList = []
    for i in range(0,len(noteNames)):
        noteList.append(Note.Note(noteNames[i],i*samp_per_note,samp_per_note,64))
    return Genome.Genome(noteList)

def make_Cmaj_up():
    note_names = ["C3","D3","E3","F3","G3","A3","B3","C4"]
    return make_Genome_from_notes(note_names)
    
def make_Cmaj_down():
    note_names = ["C3","D3","E3","F3","G3","A3","B3","C4"]
    note_names.reverse()
    return make_Genome_from_notes(note_names)

def make_ttls():
    startTimes = np.array([2.69e4,5.28e4,7.97e4,1.06e5,1.32e5,1.59e5,1.84e5,2.39e5,2.66e5,2.90e5,3.17e5,3.43e5,3.67e5,3.92e5])
    stopTimes = np.array([4.58e4,7.00e4,9.87e4,1.22e5,1.50e5,1.75e5,2.29e5,2.61e5,2.84e5,3.16e5,3.41e5,3.65e5,3.91e5,4.39e5])
    noteNames = ["G3","G3","D4","D4","E4","E4","D4","C4","C4","B3","B3","A3","A3","G3"]
    noteList = []
    for i in range(0,len(noteNames)):
        noteList.append(Note.Note(noteNames[i],startTimes[i],stopTimes[i]-startTimes[i],64))
    return Genome.Genome(noteList)

def draw_midi(gen):
    #Set up grid
    Ymax = len(parameters.notes)
    Xmax = int(np.ceil(parameters.MAX_SONG_TIME))

    plt.figure(figsize=(12,8))
    ax = plt.subplot(1,1,1)
    ax.set_xticks(range(0, Xmax))
    ax.set_yticks(range(0, Ymax+1))
    ax.yaxis.set_major_formatter(ticker.NullFormatter())
    ax.set_yticks(np.arange(0,Ymax)+0.5,labels=parameters.notes,va='center',fontsize=8,minor=True)
    ax.tick_params(axis='y', which='minor', tick1On=False, tick2On=False)
    ax.set_xlim((-0.1, Xmax))
    ax.set_ylim((-0.1, Ymax))
    ax.set_axisbelow(True)
    ax.grid(alpha=0.5)
    ax.set_xlabel("Time (Seconds)")

    #Colors for velocity
    norm = mpl.colors.Normalize(vmin=0, vmax=parameters.MAX_VELOCITY)
    m = cm.ScalarMappable(norm=norm, cmap=cm.YlOrRd)

    #plot notes
    for n in gen.noteList:
        name = n.noteName
        idx = parameters.notes.index(name)
        #lower left, upper left, upper right, lower right
        ypos = [idx,idx+1,idx+1,idx]
        xleft = n.startTime/parameters.SAMPLE_RATE
        xright = (n.startTime+n.duration)/parameters.SAMPLE_RATE
        xpos = [xleft,xleft,xright,xright]
        rgb = m.to_rgba(n.velocity)[:3]
        ax.fill(xpos,ypos,mpl.colors.rgb2hex(rgb))
    plt.show()

def process_wav(readpath):
    samplerate, data = wavfile.read(readpath)
    #print(samplerate)
    if(not samplerate==parameters.SAMPLE_RATE):
        print("ERROR: INPUT WAV IS NOT SAMPLED AT 44100 HZ")
        return
    dim = data.ndim
    if(dim==2):
        data = ((data[:,0]+data[:,1])/2).astype(np.int16) #stereo to mono
    N = parameters.MAX_SAMPLES
    if (len(data)>N):
        data = data[:N] #cut to 10 seconds
    elif (len(data)<N):
        data = np.concatenate((data,np.zeros(N-len(data))))
    return data

def downsample(signal): #downsample 44.1kHz by factor of 10 -> fs = 4410 Hz
    return (sig.decimate(signal,parameters.DOWNSAMPLE_FACTOR), int(parameters.SAMPLE_RATE/parameters.DOWNSAMPLE_FACTOR))

#Get Spectrogram of downsampled signal
def calc_spectrogram(time_seq_ds):
    '''
    time_seq_array = np.zeros((parameters.FRAME_SAMPLES,parameters.NUM_FRAMES)) #matrix with each col = 4096 time samples, 50% overlap
    for i in range(0,parameters.NUM_FRAMES): #parse time data into array
        start_idx = int(i*(1-parameters.FRAME_OVERLAP)*parameters.FRAME_SAMPLES)
        time_seq_array[:,i] = time_seq[start_idx:start_idx+parameters.FRAME_SAMPLES]
    freqs,spgram = sig.periodogram(time_seq_array,parameters.SAMPLE_RATE,'hann')
    '''
    noverlap = int(parameters.FRAME_OVERLAP*parameters.FRAME_SAMPLES)
    nfft = 4*parameters.FRAME_SAMPLES #gives 2.15 Hz resolution
    (f,t,Sxx) = sig.spectrogram(x=time_seq_ds,fs=parameters.DOWNSAMPLE_FS,window='hann',nperseg=parameters.FRAME_SAMPLES,noverlap=noverlap,nfft=nfft)
    return (f,t,Sxx)

def normalize_spec_frames(Sxx): #Normalize Spectrogram time frames between each other
    #rescale all frames so that mean of frame i = mean of all frames up to i
    (m,n) = Sxx.shape
    Sxx_means = np.mean(Sxx,axis=0)#column average
    Sxx_mean_cumsums = np.cumsum(Sxx_means)
    Nxx = np.zeros((m,n))
    for i in range(0,n):
        running_avg = Sxx_mean_cumsums[i]/(i+1)
        rescale_factor = running_avg/Sxx_means[i]
        if(rescale_factor<(1/parameters.MAX_RESCALE_FACTOR)):
            rescale_factor=(1/parameters.MAX_RESCALE_FACTOR)
        elif(rescale_factor>parameters.MAX_RESCALE_FACTOR):
            rescale_factor=parameters.MAX_RESCALE_FACTOR
        Nxx[:,i] = rescale_factor*Sxx[:,i]
    return Nxx
    pass