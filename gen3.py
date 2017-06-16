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

    FORMAT_GRAND = '''\\version "2.16.2"
    {
    \\new PianoStaff 
        <<
        \\new Staff { \\time 4/4
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
    \\new Staff { \\clef "treble" \\time 4/4
                 %s
                }
    \\new Staff { \\clef "treble" 
                 %s
                }
    >>
    }
    '''
    def __init__(self, format='Grand', tRange=(0,4), bRange=(4,8), notes=16, barPerLine=4):
        self.format = format
        self.tRange = tRange
        self.bRange = bRange
        self.numNotes = notes
        self.barPerLine = barPerLine
        random.seed(datetime.now())

    def printGrand(self):
        print( SightGen.FORMAT_GRAND % (self.tNoteString, self.bNoteString))

    def print2Treble(self):
        print( SightGen.FORMAT_2TREBLE % (self.tNoteString, self.bNoteString))

    def genNotes(self):
        random.seed(datetime.now())
        tNotesIndex = [ random.randrange(self.tRange[0], self.tRange[1]+1) for i in range(self.numNotes) ]
        random.seed(datetime.now())
        bNotesIndex = [ random.randrange(self.bRange[0], self.bRange[1]+1) for i in range(self.numNotes) ]

        tNoteList = [ SightGen.TN[i] for i in tNotesIndex ]
        bNoteList = [ SightGen.TN[i] for i in bNotesIndex ]

        # Insert \\break for each of x bar assume 4/4
        tNoteList = [ l+' \\break'*(n%(self.barPerLine*4) == self.barPerLine*4-1) for n, l in enumerate(tNoteList) ]
        bNoteList = [ l+' \\break'*(n%(self.barPerLine*4) == self.barPerLine*4-1) for n, l in enumerate(bNoteList) ]

        tNoteString = ' '.join(tNoteList)
        bNoteString = ' '.join(bNoteList)

        self.tNoteString = tNoteString
        self.bNoteString = bNoteString

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
    parser.add_argument('-n', '--number', type=SightGen.noteNum, default=48)
    parser.add_argument('-T', '--Treble', nargs=2, type=int, default=(7,11))
    parser.add_argument('-B', '--Bass', nargs=2, type=int, default=(0,4))
    parser.add_argument('-b', '--bar', type=int, default=4)

    parser.epilog='''
    Generate Random Notes In Lilypond
                   The position of each notes are index in the list with follwoing reference
                   0  --> Lowest C (2 lines below Bass Clef) --> C2
                   14 --> Middle C --> C4
                   28 --> Highest C ( 2 lines above Treble Clef) --> C6
                   (4 ,10) --> Bass Clef 
                   (16,24) --> Treble Clef 
                   '''
    args = parser.parse_args()

    gen = SightGen(format=args.format, tRange=args.Treble, bRange=args.Bass,  notes=args.number,
            barPerLine=args.bar)
    gen.genSheet()
