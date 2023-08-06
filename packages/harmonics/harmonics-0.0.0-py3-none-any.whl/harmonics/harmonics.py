import yaml
import numpy as np
import pandas as pd
from mido import MidiFile
import mido
import time
import numba
import os
from dataclasses import dataclass

# from element import *
# from properties import *
# from part import *
# from voice import *
# from tune import *
# from audio import *
# from midi import *
# from bot import *
# from dataclasses import dataclass

def timer(string,t):
    print(f"{string} took {time.time() - t} seconds")
    return time.time()




class Music:
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    CONFIG_PATH =  os.path.join(ROOT_DIR,'config.yaml')
    with open(CONFIG_PATH, "r") as f:
        CFG = yaml.safe_load(f)
    IDICT : dict = {k:v for k,v in zip(CFG['INAMES'],CFG['IDIST'])}
    EDICT : dict = {k:v for k,v in zip(CFG['INAMES'],CFG['EXTENSION'])}
    NDICT : dict = {k:v for k,v in zip(CFG['NOTES'],CFG['NDIST'])}
    INAMES    : dict =  CFG['INAMES']
    INTERVALS : dict =  CFG['INTERVALS']
    SCALES    : dict =  CFG['SCALES']
    CHORDS    : dict =  CFG['CHORDS']
    PATTERNS  : dict =  CFG['PATTERNS']
    FORMULAS  = {**SCALES,**CHORDS,**PATTERNS}
    TUNING    : dict =  CFG['TUNING']
    INSTRUMENTS   : dict =  CFG["INSTRUMENTS"] 
    MIDI_CHANNELS : dict =  CFG['MIDI_CHANNELS']
    MIDI_GM1      : dict =  CFG['MIDI_GM1']
    MIDI_GM2      : dict =  CFG['MIDI_GM2']
    MIDI_CC       : dict =  CFG['MIDI_CC']
    DRUM_PROG     : dict = CFG['DRUM_PROG']
    DRUM_KEYMAP   : dict =  CFG['DRUM_KEYMAP']
    DEF_OCTAVE = 4
    DEFAULT_KEY = 'C'
    MIDIMESSAGE = CFG['MIDIMESSAGE']
    
    @classmethod
    def quantitize(cls,n):
        bins = np.array([0, 0.125, 0.29, 0.4, 0.58, 0.7, 0.875])
        vals = np.array([0, 0.25,  0.33, 0.5, 0.66, 0.75, 0])
        return vals[np.digitize(n,bins)-1]

    @classmethod
    def midi_cc(cls,data1):
        return Music.MIDI_CC.get(data1)
    
    @classmethod
    def midi_program(cls,channel,data1):
        if channel == 9:
            return Music.DRUM_PROG.get(data1)
        else:
            return Music.MIDI_GM1.get(data1)
    
    @classmethod
    def midi_drum(cls,midi):
        return Music.DRUM_KEYMAP.get(midi)
        
    @classmethod
    def _list(cls,thing):
        if type(thing) in (tuple,list,np.ndarray): return thing
        if type(thing) in (str,float,str): return [thing]


class Context():
    "Harmonic, rhytmic context for a note, used in Part and Song."
    def __init__(self,key='C',mode=1,time_signature='4:4',chord=None):
        self.key            = key
        self.mode           = mode
        self.time_signature = time_signature
        self.chord          = chord
    
    def __eq__(self, context):
        if isinstance(context, Context):
            return (self.key == context.key) & (self.mode == context.mode) & (self.time_signature == context.time_signature) & (self.chord == context.chord)
        
        
        
class Instrument():
    """Mainly a property of a part."""
    
    def __init__(self,name=None,channel=None,bank=None,instrument_type=None):
        self.name = name
        self.channel = channel
        self.bank = bank
        self.instrument_type = instrument_type
        
class Interval():
    
    """Encapsulates the concept of an interval."""
    
    def __init__(self,name):
        if isinstance(name,Interval):
            self.__dict__.update(vars(name))
            return
        else:
            if name in Music.INAMES: 
                self.name     = name
                self.distance  = Music.IDICT[name]
                if int(self.name.split('b')[-1].split('#')[-1]) > 7: self.distance += 12
            else: 
                if type(name) in [tuple,list]:
                    if len(name) == 2 and type(name[0]) == Note:
                        self.distance = name[1].midi - name[0].midi  
                else: self.distance  = name
                candidates     = [a for a,b in Music.IDICT.items() if b == self.distance%12]
                if self.distance >12:
                    candidates = [c for c in candidates if self.Music.EDICT[c] in (1,2)]
                elif self.distance <12:
                    candidates = [c for c in candidates if self.Music.EDICT[c] in (0,2)]
                self.name      = candidates[0]
            self.other_names   = [a for a,b in Music.IDICT.items() if b == self.distance%12]
            for a in Music.INTERVALS.keys():
                self._detect(a)
            self.octave = (self.distance//12)
    
    def _detect(self,class_attribute):
        if type(Music.INTERVALS[class_attribute][0]) == str:
            attribute = self.name
        else:
            attribute = self.distance
        if attribute in Music.INTERVALS[class_attribute]:
            self.__dict__[class_attribute.lower()] = True
        else:
            self.__dict__[class_attribute.lower()] = False
    
    def __repr__(self): return self.name
    def __str__(self): return self.name
    
    def __eq__(self,interval):
        if isinstance(interval, Interval):
            return self.distance == interval.distance
        elif type(interval) == str:
            return self.distance == Interval(str)
        else:
            return self.distance == interval
        
    def __add__(self,interval):
        if type(interval)  == Interval: return Interval(self.distance + interval.distance)
        elif type(interval) == int: return Interval(self.distance + interval)
    
    
    def __sub__(self,interval):
        if type(interval) == Interval: return Interval((self.distance - interval.distance)%12)
        elif type(interval) == int: return Interval((self.distance - interval)%12)
    

    def __invert__(self):
        if self.distance <  0: return Interval(abs(self.distance-12)%12)
        if self.distance >  0: return Interval(abs(self.distance+12)%12)
        if self.distance == 0: return Interval(0) 
        
class Pattern():
    
    """A sequence of intervals."""
    
    @classmethod
    def find_pattern(cls,arr,seq):
        Na, Nseq = arr.size, seq.size
        r_seq = np.arange(Nseq)
        M = (arr[np.arange(Na-Nseq+1)[:,None] + r_seq] == seq).all(1)
        if M.any() >0:
            return np.where(np.convolve(M,np.ones((Nseq),dtype=int))>0)[0]
        else:
            return []
    
    def __init__(self,name='',notes=None,intervals=None):
        self.name = name ; self.notes = notes ; self.intervals = intervals
        if notes:
            try:
                self.intervals = [a//b for a,b in zip(notes,notes[1:])]
                self.distance = np.array([i.distance for i in self.intervals])
            except TypeError: pass
        elif name:
            try:
                intervals_from_start = {Interval(i) for i in Music.FORMULAS[self.name]}              
                self.distance  = np.array([(b-a).distance for a,b in zip(intervals_from_start,intervals_from_start[1:])])
                self.intervals = [Interval(i) for i in self.distance] 
            except KeyError: pass
        else:
            return
     
    def __repr__(self) : return '--'+'--'.join([str(i) for i in self.distance])+'--'
    def __str__(self):   return '--'+'--'.join([str(i) for i in self.intervals])+'--' 
    
    
class Pitch:
    
    @classmethod
    def midi_to_note(cls,midi):
        return [a for a,b in Note.NDICT.items() if midi%12 == b][0]
    @classmethod
    def midi_octave(cls,midi):
        return (midi//12)-1
    @classmethod 
    def midi_to_name(cls,midi):
        return ''.join([cls.midi_to_note(midi),str(cls.midi_octave(midi))])
    @classmethod 
    def freq2pitch(cls,freq): return round(np.log2(freq/440)*12+69)
    @classmethod 
    def pitch2freq(cls,pitch): return 440*np.power(2,(pitch-69)/12)
    
    def __init__(self,n):
        if type(n) in [int,float]:
            self.midi   = n
        elif type(n) == str:
            if n[-1] == 'z':
                self.frequency = float(n[:-2])
                self.midi = Pitch.freq2pitch(self.frequency)
            else:
                if n[-1].isnumeric():
                    self.octave = int(n[-1])
                    self.name = n[:-1]
                else:
                    self.name = n
                    self.octave = Note.DEF_OCTAVE
                self.midi = Note.NDICT[self.name] + (self.octave+1)*12
        else:
            print('wut?')
        if 'name' not in self.__dict__:   self.name   = Pitch.midi_to_note(self.midi)
        if 'octave' not in self.__dict__: self.octave = Pitch.midi_octave(self.midi)
        # computed
        self.equivalents = [a for a,b in Note.NDICT.items() if self.midi%12 == b]
        self.pitch_class = Note.NDICT[self.name]
        if 'frequency' not in self.__dict__: self.frequency = Pitch.pitch2freq(self.midi)
        self.offpitch  = f'{1200*np.log2(self.frequency/Pitch.pitch2freq(self.midi))} cents'
        
    def __repr__(self): return self.name
    
class Duration:
    def __init__(self,duration):
        self.duration = duration
        
    def __repr__(self): return str(self.duration)+' beat(s)'
    
class Volume:
    def __init__(self,velocity):
        self.velocity = velocity
    def __repr__(self): return str(self.velocity)
    
class Mod:
    def __init__(self,mod):
        self.mod = mod
    def __repr__(self): return str(self.mod)

@dataclass
class NoteData:
    message_type: str
    instrument:      int
    pitch:        int
    volume:        int
    duration:     float


class Note:
    is_note = True
    DEF_OCTAVE = Music.DEF_OCTAVE
    NDICT = Music.NDICT
    
    @classmethod
    def fromData(cls,obj):
        if obj.message_type == 'note_on':
            #need to convert duration and maybe change channel to instrument
            return cls(obj.pitch,
                       volume     = obj.volume,
                       duration   = obj.duration,
                       instrument = obj.instrument)
    
    def __init__(self,n,
                 duration    = 1, #unit?
                 volume      = 100, #units
                 mod         = None,
                 kind        = None,
                 instrument  = 0):
        self.pitch      = Pitch(n)
        self.duration   = Duration(duration)
        self.volume     = Volume(volume)
        self.mod        = Mod(mod)
        self.type       = kind
        self.instrument = Instrument(instrument)
    
    def __eq__(self,note):
        return self.pitch == note
        
    def __floordiv__(self,note):
        if isinstance(note, Note):
            return Interval([self.pitch,note.pitch])  
    
    def __truediv__(self,note):
        if isinstance(note, Note):
            distance = Interval([self.pitch,note.pitch]).distance
            octaves  = distance // 12 ; semis = distance % 12
            return f"{octaves} octaves and {semis} semitones"                    
    
    def __str__(self):  return repr(self.pitch)
    def __repr__(self): return repr(self.pitch)
    def __len__(self):  return self.pitch.midi
    def __add__(self,note):
        if type(note) == Interval: return Note(n          = self.pitch.midi+note.distance,
                                               duration   = self.duration,
                                               volume     = self.volume,
                                               mod        = self.mod)
        if type(note) == Note:
            return Sequence(notes=[self,note])
        
            
    def enharmonic(self,spelling='b',name=''):
        if (name != '') and name in self.pitch.equivalents:
            self.name = name
        if spelling == 'natural': selection = [i for i in self.pitch.equivalents if ('b' not in i) & ('#' not in i)]
        else: selection = [i for i in self.pitch.equivalents if spelling in i]
        if len(selection):
            self.name = selection[0]
    
    
    def append(self,note):
        if type(note) == Note: return Sequence(notes=[self,note])
        
    def to_data(self):
        #if mod also return CC message
        return NoteData('note_on', self.instrument.name, self.pitch.midi, self.volume.velocity, self.duration.duration)

class Chord(Note):
    DEFAULT_ROOT = Music.DEFAULT_KEY
    CHORDS   = {k : [Interval(i) for i in v[0]] for k,v in Music.CHORDS.items()}
    
    def __init__(self,chord='',notes=None,root='',key=''):
        self.key  = key
        self.root = root
        if chord:
            self.chord = chord
            self.formula = self.CHORDS[chord]
            if not self.root: self.root = Chord.DEFAULT_ROOT
            self.notes   = [Note(i) for i in [Note(self.root).midi + i.distance for i in self.formula]]
        elif notes:
            pass
        self.respell()
        if not self.root:
            pass
        
    def respell(self):
        if not self.key:
            def _respell(acc):
                for n in self.notes: n.enharmonic(spelling=acc)
            if ('b' in self.root) or ('b' in ' '.join([i.name for i in self.formula])): _respell('b')
            if ('#' in self.root) or ('#' in ' '.join([i.name for i in self.formula])): _respell('#')
            _respell('natural')
        if self.key:
            pass #right spelling depending on the key

class Sequence():
    """Melody, bassline or drum part."""
    
    DEFAULT_REF = Music.DEFAULT_KEY
    
    def __init__(self,notes=None,key=None):
        super().__init__()
        self.notes    = notes
        self.key = key 
        if not self.key: self.key = self.DEFAULT_REF
        self.part_type = None
        self.respell()
    
    def __getitem__(self,index):
        if type(index) == int: return self.notes[index]
        return Sequence(notes=self.notes[index],key=self.key,part_type=self.part_type)
    
    def __add__(self,obj):
        if isinstance(obj, Sequence):
            return Sequence(notes=self.notes+obj.notes,part_type=self.part_type,key=self.key)
        if isinstance(obj, Note):
            print(self.notes)
            print(obj)
            return Sequence(notes=self.notes+[obj],part_type=self.part_type,key=self.key)
            
    def __contains__(self,note):
        return [note==n for n in self.notes]                

    def __repr__(self):
        return str(self.notes)
    
    @property
    def df(self):
        df = pd.DataFrame([i.to_data() for i in self.notes])
        df['beat_time'] = 0###########################################""
        df['_miditime']  = [0]+df._duration.to_list()[:-1]
        
    
    def respell(self,names=[]):
        if names:
            for name in names:
                for note in self.notes:
                    note.enharmonic(name=name)
        else:
            def _respell(acc):
                for n in self.notes: n.enharmonic(spelling=acc)
            if 'b' in str(self.key): _respell('b')
            if '#' in str(self.key): _respell('#')
            _respell('natural')

     
class Tune():
    def __init__(self,path=None,bpm=None,key='',time_signature=(4,4)):
        super().__init__()
        self.info = []
        self.path = path
        self.bpm = bpm
        self.tempo = self._midi_get('tempo',bpm=self.bpm)
        self.time_signature = time_signature
        if self.path:
            self.MIDI = MidiFile(path,clip=True)
            start = time.time()
            self._extract_midi()
            timer('extraction', start)
        else:
            self.MIDI = None
            self.__dict__.update({i:None for i in ['key_signature','channel_list','df','tracks','parts']})
            
    def __repr__(self):
        return f"""\
path:     {self.path}
bpm:      {self._bpm}
key:      {self.key_signature}
time_sig: {self.time_signature} 
channels: {self.channel_list}
"""
            
    @property
    def bpm(self):
        return self._bpm
    @bpm.setter
    def bpm(self, val):
        self._bpm = val
        self._tempo = self._midi_get('tempo',bpm=self._bpm)

    @property
    def tempo(self):
        return self._tempo
    @tempo.setter
    def tempo(self, val):
        self._tempo = val
        self._bpm = self._midi_get('bpm',tempo=self._tempo)       
        
    @property
    def ticks_per_beat(self):
        return self.MIDI.ticks_per_beat
    
    @property
    def df(self):
        return self._df[[i for i in self._df.columns if i[0] != '_']]
    
    @property
    def instr(self):
        return {i: [a for a in set(self._df[self._df.channel == i].instr) if type(a) != float] #removes np.nan
                    for i in self.channel_list}

    def notes(self,channel='all'):
        if channel == 'all': return self.df[self._df.type == 'note_on']
        else: return self.df[(self._df.type == 'note_on') & (self._df.channel == channel)]
    
    def channel(self,channel,meta=False):
        df = self.df[self.df.channel == channel]
        if not meta: return df[(df.type == 'note_on') | (df.type == 'note_off')]
        else: return df
        
    def cc(self,channel=None):
        df = self.df[self.df.type == 'CC']
        if channel: return df[df.channel == channel]
        else: return df
    
    def prog(self,channel=None):
        df = self.df[self.df.type == 'program']
        if channel: return df[df.channel == channel]
        else: return df
                     
    def get(self,c=None,t=None):
        if len(self._df):
            if c and t: return self._df[(self._df.channel == c) & (self._df.type == t)]
            if c: return self._df[(self._df.channel == c)]
            if t: return self._df[(self._df.type == t)]
    
    def __getitem__(self,number):
        if type(number) == int:
            return None
    
    def _midi_get(self,string,tempo=None,bpm=None,beats=None,ticks_per_beat=None,ticks=None,ceil=False,time_signature=None):
        if string == 'bpm' and tempo: return int(mido.tempo2bpm(tempo))
        if string == 'tempo' and bpm: return mido.bpm2tempo(bpm)
        if string == 'beats' and ticks_per_beat and ticks:
            if ceil: return np.ceil(ticks/ticks_per_beat)
            else: return ticks/ticks_per_beat
        if string == 'ticks' and beats and ticks_per_beat: return beats*ticks_per_beat
        if string == 'bar' and time_signature and beats:
            if ceil: return np.ceil(beats/int(time_signature.split(':')[0])) 
            else: return beats/int(time_signature.split(':')[0])
        else: return None
    
    def _extract_midi(self):
        tracks = []
        for n,track in enumerate(self.MIDI.tracks):
            _miditime = np.array([i.time for i in track]).astype(np.int32)
            time_to_next = np.hstack((_miditime[1:],[0])).astype(np.int32)
            #time_to_next = np.array([i.time for i in track])
            tick_time = np.cumsum(_miditime).astype(np.int32)
            msg = np.array([i.hex() for i in track])
            msgtranslate = Music.MIDIMESSAGE
            df = pd.DataFrame({'track': [n]*len(time_to_next),
                          'type':    np.array([msgtranslate[i[0]] for i in msg]),
                          'channel':      np.array([int(i[1],16) for i in msg],dtype=np.int32),
                          'data1':        np.array([int(i[3:5],16) for i in msg],dtype=np.int32),
                          'data2':        np.array([int(i[6:],16) if len(i[6:])==2 else 999 for i in msg],dtype=np.int32),
                          '_miditime':     _miditime,
                          '_duration':     time_to_next,
                          'tick_time':    tick_time,
                          '_hex_msg':      msg})
            off = df[(df.type == 'note_on')&(df.data2 == 0)].index.values
            df.loc[off,'type'] = 'note_off'
            tracks.append(df)
        if len(tracks) == 1: self._df = tracks[0]
        else: self._df = pd.concat(tracks)
        self._df.reset_index(inplace=True,drop=True)
        
        # EXTRACT METAMESSAGES
        self.channel_list = list(set(self._df.channel))
        self.metamessages = {a.type : a for a in [i for a in self.MIDI.tracks for i in a if i.is_meta]}
        if 'time_signature' in self.metamessages:
            ts = self.metamessages['time_signature']
            self.time_signature = (ts.numerator,ts.denominator)
        else:
            self.time_signature = (4,4) ; self.info.append('No time signature in MIDI file, default selected.')
        if 'set_tempo' in self.metamessages: self.tempo = self.metamessages['set_tempo'].tempo
        else: self.info.append('No tempo in MIDI file.')
        if 'key_signature' in self.metamessages: self.key_signature = self.metamessages['key_signature'].key
        else: self.key_signature = '' ; self.info.append('No key signature in MIDI file')
        
        #COMPUTING RELEVANT INFO

        self._df['beat_time']     = np.round(self._df.tick_time/self.MIDI.ticks_per_beat,2)
        self._df['_beat_pos']      = np.round(self._df.beat_time.to_numpy()%1,2)
        f = Music.quantitize
        self._df['q_beat_p']      = f(self._df._beat_pos.to_numpy())
        self._df['_curr_beat']     = np.floor(self._df.beat_time.to_numpy()).astype(np.int32)+1
        self._df['rel_beat']      = ((self._df._curr_beat.to_numpy() - 1)%self.time_signature[0])+1
        self._df['_bar_time']      = np.round(self._df.beat_time.to_numpy()/self.time_signature[0],2)
        self._df['curr_bar']      = np.array(((self._df._curr_beat - 1)/self.time_signature[0])+1,dtype=np.int32)
        self._df['bar_pos']       = np.round(self._df._bar_time.to_numpy()%1,2)
        
        # TRANSLATE NOTES
        vm = np.vectorize(Pitch.midi_to_note)
        vd = np.vectorize(Music.midi_drum)
        midx = self._df[self._df.channel != 9].index ; didx = self._df[self._df.channel == 9].index
        if len(midx): self._df.loc[midx,'note'] = vm(self._df.loc[midx,'data1'].to_numpy())
        if len(didx): self._df.loc[didx,'note'] = vd(self._df.loc[didx,'data1'].to_numpy())
        else: self._df.loc[:,'note'] = np.nan
        
        # GET NOTE DURATION
        for c in self.channel_list:
            df = self.channel(c)
            for n in set(df.data1):
                d = df[df.data1 == n]
                #assert len(d[d.type == 'note_on']) == len(d[d.type == 'note_off'])
                idx_on = d[d.type == 'note_on'].index
                idx = list(zip(idx_on,d[d.type == 'note_off'].index))
                _ntdur = np.array([(d.loc[b,'tick_time']-d.loc[a,'tick_time']) for a,b in idx],dtype=np.int32)
                for n,i in enumerate(idx_on):
                    self._df.loc[i,'_ntdur'] = int(_ntdur[n])
        
        # TRANSLATE PROGRAM CHANGES AND CCS
        vcc = np.vectorize(Music.midi_cc)
        cc_idx = self._df[self._df.type == 'CC'].index
        if len(cc_idx):
            self._df.loc[cc_idx,'cc'] = vcc(self._df.loc[cc_idx,'data1'].to_numpy())
        else: self._df.loc[:,'cc'] = np.nan
        vpr = np.vectorize(Music.midi_program)
        pr_idx = self._df[self._df.type == 'program'].index
        if len(pr_idx):
                self._df.loc[pr_idx,'instr'] = vpr(self._df.loc[pr_idx,'channel'].to_numpy(),
                                        self._df.loc[pr_idx,'data1'].to_numpy())
        else:
            self._df.loc[:,'instr'] = np.nan
                
        

    def export(self,path):
        """wrapper for mido object"""
        pass
    
    def add_phrase(self,Phrase):
        pass
        

            



        
