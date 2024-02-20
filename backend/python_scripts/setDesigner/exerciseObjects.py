import abjad
import math
from setDesigner.musicObjects import Scale
from decimal import Decimal

class Exercise:
    def __init__(
        self,
        pitchPattern,
        rhythmPattern,
        key,
        mode,
        preamble,
    ):
        self.__pitchPattern = pitchPattern
        self.__rhythmPattern = rhythmPattern
        self.__key = key
        self.__mode = mode
        self.__preamble = preamble

    def notationPattern(self):
        if self.__pitchPattern.get('repeatMe') is not True:
            notationPattern = []
        else:
            notationPattern = ["repeat"]
        rhythms = self.__rhythmPattern.get('rhythmPattern')
        notes = self.__pitchPattern.get('notePattern')
        noteIndex = 0
        for r in rhythms:
            if r[0].isnumeric():
                notationPattern.append([notes[noteIndex], r[0]])
                noteIndex += 1
            elif r == ["~"]:
                noteIndex -= 1
            else:
                notationPattern.append(r)

        returnPattern = [notationPattern]
        if self.__pitchPattern.get('holdLastNote') is True:
            heldNoteRhythm = "1"
            if self.__rhythmPattern.get('timeSignature') == (4, 4):
                heldNoteRhythm = "1"
            returnPattern.append([notes[-1], heldNoteRhythm])
        return returnPattern

    def createRepeatPhrase(self, scaleNotes, notes):
        container = abjad.Container("")
        for note in notes:
            if isinstance(note[0], int):
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
        return pitchName + note[1] + " "

    @property
    def buildScore(self):
        container = abjad.Container("")
        scaleNotes = self.getScaleNotes()
        pattern = self.notationPattern()
        for group in pattern:
            if group[0] == "repeat":
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
                abjad.NamedPitchClass(self.__key), abjad.Mode(self.__mode)
            )
            abjad.attach(keySignature, attachHere)
            ts = tuple(int(x) for x in self.__rhythmPattern.get('timeSignature'))
            timeSignature = abjad.TimeSignature(ts)
            abjad.attach(timeSignature, attachHere)
            if not abjad.get.indicators(container[-1], abjad.Repeat):
                bar_line = abjad.BarLine("|.")
                last_leaf = abjad.select.leaf(container[-1], -1)

                if last_leaf is not None:
                    abjad.attach(bar_line, last_leaf)
                else:
                    print("No suitable leaf for bar line attachment found in the last container.")

        if self.__rhythmPattern.get('articulation'):
            for articulation in self.__rhythmPattern.get('articulation'):
                if articulation.get("articulation").lower() == "fermata":
                    a = abjad.Fermata()
                    abjad.attach(a, container[0][int(articulation.get("index"))])

        voice = abjad.Voice([container], name="Exercise_Voice")
        staff = abjad.Staff([voice], name="Exercise_Staff")
        score = abjad.Score([staff], name="Score")
        return score

    def getScaleNotes(self):
        scale = Scale(self.__key + "'", self.__mode)
        scaleNotes = scale.makeScale()
        return scaleNotes