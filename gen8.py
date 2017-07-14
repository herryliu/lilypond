#!/usr/bin/python

# the program is to generate random notes for treble/bass clef to imporve the sight reading skill
import random
import argparse
from datetime import datetime

class SightGen:
    ''' variables: tNotes --> List to hold the treble clef notes
                   bNotes --> List to hold the bass clef notes
                   tRange, bRange --> List to starting note and ending note
                   The list holding 4x Octaves.
                   0 - 6 --> 1st Octave
                   7 -13 --> 2nd Octave
                   14-20 --> 3rd Octave (middle C)
                   21-27 --> 4th Octave
                   28-34 --> 5th Octave

                   (4 ,10) --> Bass Clef
                   (16,24) --> Treble Clef

                   14 --> Middle C
                   0  --> Lowest C (2 lines below Bass Clef)
                   28 --> Highest C ( 2 lines above Treble Clef)
    '''

    TN = ["c,", "d,", "e,", "f,", "g,", "a,", "b,",
        "c", "d", "e", "f", "g", "a", "b",
        "c'", "d'", "e'", "f'", "g'", "a'", "b'",
        "c''", "d''", "e''", "f''", "g''", "a''", "b''"]

    R4Dict = {
            # 1/4 notes only
            (4,1):[['4', '4', '4','4'],],

            # 4x 1/4, 1x 1, 2x 1/2, 1x 3/4 + 1x 1/4, 1x 1/4 + 1* 3/4
            (4,2):[['4', '4', '4','4'],
                    ['1'],
                    ['2', '2'],
                    ['2.', '4'],
                    ['4', '2.'],
                ],
            # 1/4 notes only
            (4,3):[['1'],],
            # 1/2 + 1/2 notes only
            (4,4):[['2','2'],],

            (4,5):[['4', '4', '4','4'],
                    ['1'],
                    ['2', '2'],
                    ['2.', '4'],
                    ['4', '2.'],
                    ['2','4','4'],
                    ['4','2','4'],
                    ['4','4','2'],
                ],
            (3,1):[['4','4','4'],],

            (3,2):[['4','4','4'],
                    ['4', '2.'],
                    ['2.','4']
                ],
             }

    FORMAT_HEADER = r'''
    #(set-default-paper-size "a4" 'landscape)
    #(set-global-staff-size 30)
    \score
    '''
    FORMAT_FOOTER = r'''
    \layout {
        \context {
            \Score
            \override SpacingSpanner #'base-shortest-duration = #(ly:make-moment 1 16)
        }
    }
    '''

    FORMAT_GRAND = '''\\version "2.16.2"
    %s
    {
    \\new PianoStaff
        <<
        \\new Staff { \\time %%s/4
                        %%s
                    }
        \\new Staff { \\clef "bass"
                        %%s
                    }
        >>
    %s
    }
    ''' % (FORMAT_HEADER, FORMAT_FOOTER)

    FORMAT_2TREBLE = '''\\version "2.16.2"
    %s
    {
    <<
    \\new Staff { \\clef "treble" \\time %%s/4
                 %%s
                }
    \\new Staff { \\clef "treble"
                 %%s
                }
    >>
    %s
    }
    ''' % (FORMAT_HEADER, FORMAT_FOOTER)


    FORMAT_BEATS = '''\\version "2.16.2"
    %s
    {
    <<
    \\new Staff { \\clef "treble" \\time \%%s/4
                 %%s
                }
    >>
    %s
    }
    ''' % (FORMAT_HEADER, FORMAT_FOOTER)


    PROFILE = {
        '1To5TwoTreble':[
            '2Treble', #format
            (21, 25),  #tRange
            (14, 18),  #bRange
            256,       #notes
            5,         #barPerLine
            4,         #time
            (1,1),         #level
        ],
        '1To5':[
            'Grand', #format
            (14, 18),  #tRange
            ( 7, 11),  #bRange
            256,       #notes
            5,         #barPerLine
            4,         #time
            (1,1),         #level
        ],
    }

    FORMAT = [ 'Grand', '2Treble', 'Beats']

    def __init__(self, format='Grand', tRange=(0,4), bRange=(4,8), notes=16, barPerLine=4,
                 time=4, level=(1,1), Profile=None, profile=None, differentNote=False):

        #List hold bars of each clef
        self.tBar, self.bBar = [], []
        #Strings generated from clef list which used to print
        self.tBarString, self.bBarString = '', ''

        if Profile == None and Profile == None:
            self.format = format
            self.tRange = tRange
            self.bRange = bRange
            self.numBars = notes
            self.barPerLine = barPerLine
            self.time = time
            self.level = level
            self.differentNote = differentNote

        if type(Profile) == str:
            self.format =     SightGen.PROFILE[Profile][0]
            self.tRange =     SightGen.PROFILE[Profile][1]
            self.bRange =     SightGen.PROFILE[Profile][2]
            self.numBars =    SightGen.PROFILE[Profile][3]
            self.barPerLine = SightGen.PROFILE[Profile][4]
            self.time =       SightGen.PROFILE[Profile][5]
            self.level =      SightGen.PROFILE[Profile][6]

        if type(profile) == int:
            p=SightGen.PROFILE.keys()[profile-1]
            self.format =     SightGen.PROFILE[p][0]
            self.tRange =     SightGen.PROFILE[p][1]
            self.bRange =     SightGen.PROFILE[p][2]
            self.numBars =    SightGen.PROFILE[p][3]
            self.barPerLine = SightGen.PROFILE[p][4]
            self.time =       SightGen.PROFILE[p][5]
            self.level =      SightGen.PROFILE[p][6]

        random.seed(datetime.now())

    def genClef(self, clef):

        # get the clif range
        # set the duration format list
        if clef == self.tBar:
            clefRange = self.tRange
            tFormList = SightGen.R4Dict[(self.time, self.level[0])]
        else:
            clefRange = self.bRange
            tFormList = SightGen.R4Dict[(self.time, self.level[1])]


        random.seed(datetime.now())
        lastPitch = None
        for k in range(0, self.numBars):
            t = random.randrange(0, len(tFormList))
            tForm = tFormList[t]
            b = random.randrange(0, len(tFormList))
            bForm = tFormList[b]

            barString = ''
            for i in range (0, len(tForm)):
                # get random tNote
                pitch = SightGen.TN[random.randrange(clefRange[0], clefRange[1]+1)]
                while self.differentNote and pitch == lastPitch:
                    pitch = SightGen.TN[random.randrange(clefRange[0], clefRange[1]+1)]
                lastPitch = pitch
                duration = tForm[i]
                note = pitch + duration
                barString = barString + note + ' '
            clef.append(barString)
            if self.barPerLine != 0 and (k+1) % self.barPerLine == 0:
                clef.append('\\break')

    def genBeats(self, clef):

        # get the clif range
        # set the duration format list
        if clef == self.tBar:
            clefRange = self.tRange
            tFormList = SightGen.R4Dict[(self.time, self.level[0])]

        random.seed(datetime.now())
        for k in range(0, self.numBars):
            t = random.randrange(0, len(tFormList))
            tForm = tFormList[t]
            barString = ''
            for i in range(0, len(tForm)):
                # get random tNote
                pitch = "b'"
                lastPitch = pitch
                duration = tForm[i]
                note = pitch + duration
                barString = barString + note + ' '
            clef.append(barString)
            if self.barPerLine != 0 and (k+1) % self.barPerLine == 0:
                clef.append('\\break')

    def genNotes(self):
        if self.format != 'Beats':
            self.genClef(self.tBar)
            self.genClef(self.bBar)
            self.tNoteString = ' '.join(self.tBar)
            self.bNoteString = ' '.join(self.bBar)
        if self.format == 'Beats':
            self.genBeats(self.tBar)
            self.tNoteString = ' '.join(self.tBar)

    def printGrand(self):
        print( SightGen.FORMAT_GRAND % (self.time, self.tNoteString, self.bNoteString))

    def print2Treble(self):
        print( SightGen.FORMAT_2TREBLE % (self.time, self.tNoteString, self.bNoteString))

    def printBeats(self):
        print( SightGen.FORMAT_BEATS % (self.time, self.tNoteString))

    def genSheet(self):
        self.genNotes()
        if self.format == '2Treble':
            self.print2Treble()

        if self.format == 'Grand':
            self.printGrand()

        if self.format == 'Beats':
            self.printBeats()

    @classmethod
    def noteNum(cls, n):
        #print("in the type check")
        n=int(n)
        if n != 4*int(n/4) or n <= 0:
            print("argument is invalid")
            raise argparse.ArgumentTypeError("The number of notes should be integer and can be devided by 4")
        return n

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate Random Notes In Lilypond",
            formatter_class=argparse.RawTextHelpFormatter
                   )

    parser.add_argument('-f', '--format', choices=SightGen.FORMAT, default='Grand')
    parser.add_argument('-n', '--number', type=int, default=16, help="in number of bars")
    parser.add_argument('-T', '--Treble', nargs=2, type=int, default=(7,11), help='treble clef notes range, defaulti (7,11)')
    parser.add_argument('-B', '--Bass', nargs=2, type=int, default=(0,4), help='bass clef notes range, default (0,4)')
    parser.add_argument('-b', '--bar', type=int, default=0, help="number of bar perline")
    parser.add_argument('-t', '--time', type=int, choices=[3,4], default=4, help='beats per bar')
    parser.add_argument('-l', '--level', nargs=2, type=int, default=[1,1], help='difficult level for treble and bass clif')
    parser.add_argument('-p', '--profile', choices=range(1, len(SightGen.PROFILE)+1), type=int, default=None,
            help='pick profile by number')
    parser.add_argument('-P', '--Profile', choices=SightGen.PROFILE.keys(), default=None,
            help='pick pofile by name')
    parser.add_argument('-u', '--unique', action='store_true', default=False, help='make adjecent notes different')

    parser.epilog='''
    Generate Random Notes In Lilypond
                   The position of each notes are index in the list with follwoing reference
                   0  --> Lowest C (2 lines below Bass Clef) --> C2
                   14 --> Middle C --> C4
                   28 --> Highest C ( 2 lines above Treble Clef) --> C6
                   (4 ,12) --> Bass Clef
                   (16,24) --> Treble Clef
    Gen 1 ... 5 and 1'... 5'
    ./gen7.py -f 2Treble -B 14 18 -T 21 25 -t 4 -l 1 1 -n 256
    ./gen7.py -p 1
    ./gen7.py -P 1To5
    ./gen8.py -f Beats -l 5 5 -n 128
                   '''
    args = parser.parse_args()
    gen = SightGen(format=args.format, tRange=args.Treble, bRange=args.Bass,  notes=args.number,
            barPerLine=args.bar, time=args.time, level=args.level, Profile=args.Profile,
                    profile=args.profile, differentNote=args.unique)
    gen.genSheet()
