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
    

def process_wav(readpath):
    samplerate, data = wavfile.read(readpath)
    #print(samplerate)
    if(not samplerate==parameters.ORIGINAL_SAMPLE_RATE):
        print("ERROR: INPUT WAV IS NOT SAMPLED AT 44100 HZ")
        return
    dim = data.ndim
    if(dim==2):
        data = ((data[:,0]+data[:,1])/2).astype(np.int16) #stereo to mono
    N = int(parameters.ORIGINAL_SAMPLE_RATE*parameters.MAX_SONG_TIME)
    if (len(data)>N):
        data = data[:N] #cut to 10 seconds
    elif (len(data)<N):
        data = np.concatenate((data,np.zeros(N-len(data))))
    return data

def downsample(signal): #downsample 44.1kHz by factor of 10 -> fs = 4410 Hz
    return sig.decimate(signal,parameters.DOWNSAMPLE_FACTOR) #IIR filtering

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
    nfft = parameters.NFFT #gives ~1 Hz separation for 4096 frame samples, 4410 fs, with hanning = 4 Hz res
    (f,t,Sxx) = sig.spectrogram(x=time_seq_ds,fs=parameters.DOWNSAMPLE_FS,window='boxcar',nperseg=parameters.FRAME_SAMPLES,noverlap=noverlap,nfft=nfft)
    return (f,t,Sxx)

def get_time_frames(time_seq_ds):
    time_seq_array = np.zeros((parameters.FRAME_SAMPLES,parameters.NUM_FRAMES)) #matrix with each col = 4096 time samples, 50% overlap
    for i in range(0,parameters.NUM_FRAMES): #parse time data into array
        start_idx = int(i*(1-parameters.FRAME_OVERLAP)*parameters.FRAME_SAMPLES)
        time_seq_array[:,i] = time_seq_ds[start_idx:start_idx+parameters.FRAME_SAMPLES]
    return time_seq_array

def normalize_frames(Sxx): #Normalize Spectrogram or Time frames between each other
    #rescale all frames so that mean of frame i = mean of all frames up to i
    (m,n) = Sxx.shape
    Sxx_means = np.mean(Sxx,axis=0)#column average
    Sxx_mean_cumsums = np.cumsum(Sxx_means)
    Nxx = np.zeros((m,n))
    for i in range(0,n):
        running_avg = Sxx_mean_cumsums[i]/(i+1)
        rescale_factor = running_avg/(Sxx_means[i]+1e-10)
        if(rescale_factor<(1/parameters.MAX_NORMALIZATION_FACTOR)):
            rescale_factor=(1/parameters.MAX_NORMALIZATION_FACTOR)
        elif(rescale_factor>parameters.MAX_NORMALIZATION_FACTOR):
            rescale_factor=parameters.MAX_NORMALIZATION_FACTOR
        Nxx[:,i] = rescale_factor*Sxx[:,i]
    return Nxx
    
def eval_note_amplitudes(Sxx): #return array of amplitudes found for each note for every frame in Sxx (Spectrogram), returns 37xNUM_FRAMES
    (m,n) = Sxx.shape
    note_amps = np.zeros((len(parameters.notes),parameters.NUM_FRAMES))
    for i in range(0,n):#each frame
        for j in range(0,len(parameters.notes)):#each note freq
            note_amps[j,i]=np.mean(Sxx[parameters.NOTE_INDICES[:,j],i])
    return note_amps

def rescale_to_target(Sxx,target_Sxx): #for each frame in Sxx, amplify so that peak matches that of target_Sxx
    Sxx_new = np.zeros_like(Sxx)
    (m,n) = Sxx.shape
    for i in range(0,n):
        scale_factor = min(np.max(target_Sxx[:,i])/(np.max(Sxx[:,i])+1e-10),parameters.MAX_RESCALE_FACTOR)
        Sxx_new[:,i] = scale_factor*Sxx[:,i]
    return Sxx_new

def attenuate_harmonics(Sxx): #attenuate everything in frame that is below 0.2*max
    Sxx_new = np.zeros_like(Sxx)
    (m,n) = Sxx.shape
    for i in range(0,n):
        max_val = np.max(Sxx[:,i])
        for j in range(0,m):
            if(Sxx[j,i]<=parameters.HARMONIC_TO_PEAK_RATIO*max_val):
                Sxx_new[j,i] = parameters.HARMONIC_ATTEN_FACTOR*Sxx[j,i]
            else:
                Sxx_new[j,i] = Sxx[j,i]
    return Sxx_new

def fit_notes(target_note_amps): #given target note amplitudes, generate genome
    (m,n) = target_note_amps.shape
    peak_amp = np.max(target_note_amps)
    cutoff = 0.2*peak_amp
    fit_noteList = []
    for i in range(0,m):
        start_frame = -1
        end_frame = -1
        for j in range(0,n):
            if(target_note_amps[i,j]>cutoff and start_frame==-1): #rising edge
                start_frame=j
            elif(target_note_amps[i,j]<cutoff and start_frame>-1 or (target_note_amps[i,j]>cutoff and start_frame>-1 and j==n-1)): #falling edge/last note
                end_frame=j
                nframes = end_frame-start_frame
                start_time = int(start_frame*parameters.FRAME_SAMPLES*(1-parameters.FRAME_OVERLAP)*parameters.DOWNSAMPLE_FACTOR)
                duration = int((parameters.FRAME_SAMPLES + (nframes-1)*parameters.FRAME_SAMPLES*(1-parameters.FRAME_OVERLAP))*parameters.DOWNSAMPLE_FACTOR)
                vel=64
                fit_noteList.append(Note.Note(parameters.notes[i],start_time,duration,vel))
                start_frame=-1
                end_frame=-1

    return Genome.Genome(fit_noteList)

def calc_precision_and_recall(target_genome,test_genome):
    recall = calc_metric(target_genome,test_genome)/len(target_genome.noteList) #percent of correct notes present in transcription
    if(len(test_genome.noteList)==0):
        precision = 0.0
    else:
        precision = calc_metric(test_genome,target_genome)/len(test_genome.noteList) #percent of transcription notes present in ground truth
    return (precision,recall)

def calc_metric(target_genome, test_genome): #test, target for precision, target, test for recall
    num_match_notes = 0
    for target_note in target_genome.noteList:
        for test_note in test_genome.noteList:
            if(test_note.noteName==target_note.noteName): #check freq match
                start_diff = np.abs(target_note.startTime-test_note.startTime)
                dur_diff = np.abs(target_note.duration-test_note.duration)
                if(start_diff<parameters.MATCH_START_TOL and dur_diff<parameters.MATCH_DUR_TOL):
                    num_match_notes+=1
                    break
        else:
            continue
    return num_match_notes

