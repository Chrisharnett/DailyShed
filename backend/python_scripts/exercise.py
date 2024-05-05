import abjad
import math
from setDesigner.musicObjects import Scale
from exerciseBucket import dropItInTheBucket
from decimal import Decimal
import os
import tempfile

GLOBAL_PREAMBLE = r"#(set-global-staff-size 28)"

class Exercise:
    def __init__(self, tonic, mode):
        self.__notePatternID = None
        self.__rhythmPatternID = None
        self.__notePattern = []
        self.__rhythmPattern = []
        self.__tonic = tonic
        self.__mode = mode
        self.__directionIndex = None
        self.__direction = None
        self.__repeatMe = False
        self.__holdLastNote = False
        self.__timeSignature = (4,4)
        self.__preamble = GLOBAL_PREAMBLE
        self.__articulation = None
        self.__exerciseID = None
        self.__filename = None
        self.__description = None
        self.__exerciseName = None

    @property
    def notePatternID(self):
        return self.__notePatternID

    @notePatternID.setter
    def notePatternID(self, notePatternID):
        self.__notePatternID = notePatternID

    @property
    def rhythmPatternID(self):
        return self.__rhythmPatternID

    @rhythmPatternID.setter
    def rhythmPatternID(self, rhythmPatternID):
        self.__rhythmPatternID = rhythmPatternID

    @property
    def notePattern(self):
        return self.__notePattern

    @notePattern.setter
    def notePattern(self, notePattern):
        self.__notePattern = notePattern

    @property
    def rhythmPattern(self):
        return self.__rhythmPattern

    @rhythmPattern.setter
    def rhythmPattern(self, rhythmPattern):
        self.__rhythmPattern = rhythmPattern

    @property
    def tonic(self):
        return self.__tonic

    @tonic.setter
    def tonic(self, tonic):
        self.__tonic = tonic

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode

    @property
    def directionIndex(self):
        return self.__directionIndex

    @directionIndex.setter
    def directionIndex(self, index):
        self.__directionIndex = index

    @property
    def directions(self):
        return self.__directions

    @directions.setter
    def directions(self, directions):
        self.__directions = directions

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        self.__filename = filename

    @property
    def exerciseID(self):
        return self.__exerciseID

    @exerciseID.setter
    def exerciseID(self, exerciseID):
        self.__exerciseID = exerciseID

    @property
    def preamble(self):
        return self.__preamble

    @preamble.setter
    def preamble(self, preamble):
        self.__preamble = preamble

    @property
    def repeatMe(self):
        return self.__repeatMe

    @repeatMe.setter
    def repeatMe(self, repeatMe):
        self.__repeatMe = repeatMe

    @property
    def holdLastNote(self):
        return self.__holdLastNote

    @holdLastNote.setter
    def holdLastNote(self, holdLastNote):
        self.__holdLastNote = holdLastNote

    @property
    def timeSignature(self):
        return self.__timeSignature

    @timeSignature.setter
    def timeSignature(self, timeSignature):
        self.__timeSignature = timeSignature

    @property
    def articulation(self):
        return self.__articulation

    @articulation.setter
    def articulation(self, articulation):
        self.__articulation = articulation

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def exerciseName(self):
        return self.__exerciseName

    @exerciseName.setter
    def exerciseName(self, exerciseName):
        self.__exerciseName = exerciseName

# The functions below create the notation image.

    def notationPattern(self):
        if not self.description:
            notationPattern = []
        else:
            notationPattern = [["repeat"]]
        notes = self.notePattern
        noteIndex = 0
        for r in self.rhythmPattern:
            if isinstance(r[0], int) or r[0].isnumeric():
                notationPattern.append([self.notePattern[noteIndex], r[0]])
                noteIndex += 1
            elif r == ["~"]:
                noteIndex -= 1
            else:
                notationPattern.append(r)

        returnPattern = [notationPattern]
        if self.description:
            heldNoteRhythm = "1"
            if self.description == (4, 4):
                heldNoteRhythm = "1"
            returnPattern.append([notes[-1], heldNoteRhythm])
        return returnPattern

    def createRepeatPhrase(self, scaleNotes, notes):
        container = abjad.Container("")
        for note in notes:
            if isinstance(note[0], (int, Decimal)):
                n = self.numberToNote(scaleNotes, note)
                container.append(n)
            elif note[0][0] == "r" and note[0] != "repeat":
                container.append(note[0])
        return container

    def createNotePhrase(self, scaleNotes, note):
        container = abjad.Container("")
        if isinstance(note[0], (int, Decimal)):
            n = self.numberToNote(scaleNotes, note)
            container.append(n)
        elif note[0][0] == "r" and note[0] != "repeat":
            container.append(note[0])
        return container

    def numberToNote(self, scaleNotes, note):
        n = int(note[0])
        pitch = ""
        octave = 0
        if n < 0:
            pitch = scaleNotes[n % 7]
            noteOctave = math.floor(n / 8)
            octave = abjad.NamedInterval(("-P" + str(7 + abs(noteOctave))))
        elif n >= 0:
            noteNumber = n % 7
            noteOctave = math.floor(n / 8)
            pitch = scaleNotes[noteNumber - 1]
        if 0 < noteOctave:
            octave = abjad.NamedInterval(("+P" + (str(7 + noteOctave))))
        pitch += octave

        pitchName = pitch.get_name()
        return pitchName + str(note[1]) + " "

    def buildScore(self):
        container = abjad.Container("")
        scaleNotes = self.getScaleNotes()
        pattern = self.notationPattern()
        p = pattern
        for index, group in enumerate(pattern):
            if isinstance(group[0], list) and group[0][0] == "repeat":
                p = group[1:]
                c = self.createRepeatPhrase(scaleNotes, group[1:])
                r = abjad.Repeat()
                abjad.attach(r, c)
                container.append(c)
            else:
                if isinstance(group[0], list):
                    container.append(self.createNotePhrase(scaleNotes, group[0]))
                else:
                    container.append(self.createNotePhrase(scaleNotes, group))

        attachHere = ""
        if len(container) >= 1:
            # attachHere = container[0]
            attachHere = container[0][0]
        if attachHere != "":
            keySignature = abjad.KeySignature(
                abjad.NamedPitchClass(self.tonic), abjad.Mode(self.mode)
            )
            abjad.attach(keySignature, attachHere)
            ts = tuple(int(x) for x in self.timeSignature)
            timeSignature = abjad.TimeSignature(ts)
            abjad.attach(timeSignature, attachHere)
            if not abjad.get.indicators(container[-1], abjad.Repeat):
                bar_line = abjad.BarLine("|.")
                last_leaf = abjad.select.leaf(container[-1], -1)

                if last_leaf is not None:
                    abjad.attach(bar_line, last_leaf)
                else:
                    print("No suitable leaf for bar line attachment found in the last container.")
        # FIXME articulation.get('articulation')???
        if self.articulation:
            for articulation in self.articulation:
                if articulation.get("articulation").lower() == "fermata":
                    a = abjad.Fermata()
                    abjad.attach(a, container[0][int(articulation.get("index"))])

        voice = abjad.Voice([container], name="Exercise_Voice")
        staff = abjad.Staff([voice], name="Exercise_Staff")
        score = abjad.Score([staff], name="Score")
        return score

    def getScaleNotes(self):
        scale = Scale(self.tonic + "'", self.mode)
        scaleNotes = scale.makeScale()
        return scaleNotes

    def createImage(self):
        score = self.buildScore()
        lilypond_file = abjad.LilyPondFile([self.preamble, score])

        # current_file_directory = os.path.dirname(__file__)
        # absolutePath = os.path.join(current_file_directory, "/", "temp/")
        # localPathOLD = os.path.join(absolutePath + self.filename)
        localPath = str(self.filename)


        abjad.persist.as_png(lilypond_file, localPath, flags="-dcrop", resolution=300)

        png = os.path.join(localPath + ".cropped.png")
        # png = os.path.join(localPath + ".cropped.png")

        dropItInTheBucket(png, localPath)
        # TODO:
        ly = os.path.join(localPath + ".ly")
        os.remove(png)
        os.remove(ly)

