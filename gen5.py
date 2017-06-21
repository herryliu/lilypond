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

    R4Dict = {(4,1):[['4', '4', '4','4'],],

              (4,2):[['4', '4', '4','4'],
                     ['1'],
                     ['2', '2'],
                     ['2.', '4'],
                     ['4', '2.'],
                    ],

              (3,1):[['4','4','4'],],

              (3,2):[['4','4','4'],
                     ['4', '2.'],
                     ['2.','4']
                    ],
             }

    FORMAT_GRAND = '''\\version "2.16.2"
    {
    \\new PianoStaff
        <<
        \\new Staff { \\time %s/4
                        %s
                    }
        \\new Staff { \\clef "bass"
                        %s
                    }
        >>
    }
    '''

    FORMAT_2TREBLE = '''\\version "2.16.2"
    {
    <<
    \\new Staff { \\clef "treble" \\time %s/4
                 %s
                }
    \\new Staff { \\clef "treble"
                 %s
                }
    >>
    }
    '''
    def __init__(self, format='Grand', tRange=(0,4), bRange=(4,8), notes=16, barPerLine=4,
                 time=4, level=1):
        self.format = format
        self.tRange = tRange
        self.bRange = bRange
        self.numNotes = notes
        self.numBars = notes
        self.barPerLine = barPerLine
        self.time = time
        self.level = level
        random.seed(datetime.now())

    def printGrand(self):
        print( SightGen.FORMAT_GRAND % (self.time, self.tNoteString, self.bNoteString))

    def print2Treble(self):
        print( SightGen.FORMAT_2TREBLE % (self.time, self.tNoteString, self.bNoteString))

    def genNotes(self):
        # set the duration format list
        tFormList = SightGen.R4Dict[(self.time,self.level)]
        # generate the bar
        tBar, bBar = [], []
        # random generate bar during form for treble and bass
        random.seed(datetime.now())
        for k in range(0, self.numBars):
            t = random.randrange(0, len(tFormList))
            tForm = tFormList[t]
            b = random.randrange(0, len(tFormList))
            bForm = tFormList[b]
            # generate treble bar
            tBarString, bBarString = '', ''
            for i in range (0, len(tForm)):
                # get random tNote
                pitch = SightGen.TN[random.randrange(self.tRange[0], self.tRange[1]+1)]
                duration = tForm[i]
                note = pitch + duration
                tBarString = tBarString + note + ' '
            tBar.append(tBarString)
            if (k+1) % self.barPerLine == 0:
                tBar.append('\\break')

            # generate bass bar
            for i in range (0, len(bForm)):
                # get random tNote
                pitch = SightGen.TN[random.randrange(self.bRange[0], self.bRange[1]+1)]
                duration = bForm[i]
                note = pitch + duration
                bBarString = bBarString + note + ' '
            bBar.append(bBarString)
            if (k+1) % self.barPerLine == 0:
                bBar.append('\\break')
        #print("tBar: %s" % tBar)
        #print("bBar: %s" % bBar)
        self.tNoteString = ' '.join(tBar)
        self.bNoteString = ' '.join(bBar)

    def genSheet(self):
        self.genNotes()
        if self.format == '2Treble':
            self.print2Treble()

        if self.format == 'Grand':
            self.printGrand()

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

    parser.add_argument('-f', '--format', choices=['Grand','2Treble'], default='Grand')
    parser.add_argument('-n', '--number', type=int, default=16, help="in number of bars")
    parser.add_argument('-T', '--Treble', nargs=2, type=int, default=(7,11))
    parser.add_argument('-B', '--Bass', nargs=2, type=int, default=(0,4))
    parser.add_argument('-b', '--bar', type=int, default=2, help="number of bar perline")
    parser.add_argument('-t', '--time', type=int, choices=[3,4], default=4)
    parser.add_argument('-l', '--level', type=int, default=1)

    parser.epilog='''
    Generate Random Notes In Lilypond
                   The position of each notes are index in the list with follwoing reference
                   0  --> Lowest C (2 lines below Bass Clef) --> C2
                   14 --> Middle C --> C4
                   28 --> Highest C ( 2 lines above Treble Clef) --> C6
                   (4 ,10) --> Bass Clef
                   (16,24) --> Treble Clef
    Gen 1 ... 5 and 1'... 5'
    ./gen5.py -f 2Treble -B 14 18 -T 21 25 -t 4 -l 1 -n 256
                   '''
    args = parser.parse_args()

    gen = SightGen(format=args.format, tRange=args.Treble, bRange=args.Bass,  notes=args.number,
            barPerLine=args.bar, time=args.time, level=args.level)
    gen.genSheet()
