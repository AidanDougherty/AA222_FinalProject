import Genome
import Note
import Individual
import parameters
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np

def make_Genome_from_notes(noteNames):
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
