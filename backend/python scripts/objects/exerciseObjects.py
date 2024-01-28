import os
import boto3
import abjad
import math
import json
from objects.musicObjects import Scale


class Exercise:
    def __init__(
        self,
        pitchPattern,
        rhythmPattern,
        key="g",
        mode="major",
        preamble=r"#(set-global-staff-size 28)",
        repeatMe=True,
    ):
        self.__pitchPattern = pitchPattern
        self.__rhythmPattern = rhythmPattern
        self.__key = key
        self.__mode = mode
        self.__preamble = preamble

    def serialize(self):
        return {
            "exerciseName": self.exerciseFileName(),
            "pitchPattern": self.__pitchPattern.serialize(),
            "rhythmPattern": self.__rhythmPattern.serialize(),
            "key": self.__key,
            "mode": self.__mode,
            "imageFileName": self.exerciseFileName() + ".cropped.png",
            "imageURL": self.imageURL(),
            "description": str(self),
        }

    @property
    def getPitchPattern(self):
        return self.__pitchPattern

    @property
    def getRhythmPattern(self):
        return self.__rhythmPattern

    def __str__(self):
        # TODO articulations, dynamics
        return f"{self.__key} {self.__mode} {str(self.__pitchPattern)} {str(self.__rhythmPattern)}."

    def notationPattern(self):
        if self.__pitchPattern.getRepeatMe is not True:
            notationPattern = []
        else:
            notationPattern = ["repeat"]
        rhythms = self.__rhythmPattern.getRhythmPattern
        notes = self.__pitchPattern.getNotePattern
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
        if self.__pitchPattern.getHoldLastNote is True:
            heldNoteRhythm = "1"
            if self.__rhythmPattern.getTimeSignature == (4, 4):
                heldNoteRhythm = "1"
            returnPattern.append([notes[-1], heldNoteRhythm])
        return returnPattern

    def exerciseFileName(self):
        return f"{self.__key}_{self.__mode}_{str(self.__pitchPattern.getPatternId)}_{str(self.__rhythmPattern.getRhythmPatternId)}"

    def imageURL(self):
        return f"https://mysaxpracticeexercisebucket.s3.amazonaws.com/{self.exerciseFileName()}"

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
        if isinstance(note[0], int):
            n = self.numberToNote(scaleNotes, note)
            container.append(n)
        elif note[0][0] == "r" and note[0] != "repeat":
            container.append(note[0])
        return container

    def numberToNote(self, scaleNotes, note):
        n = note[0]
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
            ts = tuple(self.__rhythmPattern.getTimeSignature)
            timeSignature = abjad.TimeSignature(ts)
            abjad.attach(timeSignature, attachHere)
            if not abjad.get.indicators(container[-1], abjad.Repeat):
                bar_line = abjad.BarLine("|.")
                abjad.attach(bar_line, container[-1][0])
        if self.__rhythmPattern.getArticulation:
            for articulation in self.__rhythmPattern.getArticulation:
                if articulation.get("articulation").lower() == "fermata":
                    a = abjad.Fermata()
                    abjad.attach(a, container[0][articulation.get("index")])

        voice = abjad.Voice([container], name="Exercise_Voice")
        staff = abjad.Staff([voice], name="Exercise_Staff")
        score = abjad.Score([staff], name="Score")
        return score

    def getScaleNotes(self):
        scale = Scale(self.__key + "'", self.__mode)
        scaleNotes = scale.makeScale()
        return scaleNotes

    def path(self):
        return os.path.join("static/img/" + self.__str__()) + ".cropped.png"

    def createImage(self):
        # score = self.buildScore()
        lilypond_file = abjad.LilyPondFile([self.__preamble, self.buildScore])
        #  It only works with absolute path here, but still places files in root instead of /temp
        # absolutePath = "/Users/christopherharnett/Library/CloudStorage/OneDrive-CollegeoftheNorthAtlantic/Documents/Software Development/ASD/Fall/Capstone 3540/reactSaxPracticeApp/backend-sax-practice/python scripts/temp/"

        current_file_directory = os.path.dirname(__file__)

        absolutePath = os.path.join(current_file_directory, "..", "temp")

        localPath = os.path.join(absolutePath + self.exerciseFileName())

        abjad.persist.as_png(lilypond_file, localPath, flags="-dcrop", resolution=300)

        # os.remove(os.path.join("static/img/" + self.exerciseFileName) + ".ly")
        s3BucketName = "mysaxpracticeexercisebucket"
        png = os.path.join(localPath + ".cropped.png")

        s3_client = boto3.client("s3")
        s3_client.upload_file(png, s3BucketName, self.exerciseFileName())

        ly = os.path.join(localPath + ".ly")

        os.remove(png)
        os.remove(ly)

        return self.imageURL()


class NotePattern:
    def __init__(
        self,
        notePatternId,
        notePatternType,
        notePattern,
        rhythmMatcher="general",
        description="",
        dynamic="",
        direction="",
        repeatMe=True,
        holdLastNote=True,
    ):
        self.__patternId = notePatternId
        self.__notePatternType = notePatternType
        self.__notePattern = notePattern
        self.__rhythmMatcher = rhythmMatcher
        self.__description = description
        self.__dynamic = dynamic
        self.__direction = direction
        self.__repeatMe = repeatMe
        self.__holdLastNote = holdLastNote

    def serialize(self):
        return {
            "notePatternId": self.__patternId,
            "notePatternType": self.__notePatternType,
            "notePattern": self.__notePattern,
            "rhythmMatcher": self.__rhythmMatcher,
            "description": self.__description,
            "dynamic": self.__dynamic,
            "direction": self.__direction,
            "repeatMe": self.__repeatMe,
            "holdLastNote": self.__holdLastNote,
        }

    @property
    def getRepeatMe(self):
        return self.__repeatMe

    @property
    def getHoldLastNote(self):
        return self.__holdLastNote

    def getRhythmLength(self):
        if self.__holdLastNote == True:
            return len(self.__notePattern) - 1
        return len(self.__notePattern)

    @property
    def getPatternId(self):
        return self.__patternId

    @property
    def getNotePatternType(self):
        return self.__notePatternType

    @property
    def getNotePattern(self):
        return self.__notePattern

    @property
    def getDescription(self):
        return self.__description

    @property
    def getRhythmMatcher(self):
        return self.__rhythmMatcher

    @property
    def getDirection(self):
        return self.__direction

    def __str__(self):
        return f"{self.__patternId}  {self.__notePattern} {self.__notePatternType} {self.__description}"


class RhythmPattern:
    def __init__(
        self,
        rhythmPatternId,
        rhythmType,
        rhythmDescription,
        rhythmPattern,
        timeSignature,
        articulation=None,
    ):
        self.__rhythmPatternId = rhythmPatternId
        self.__rhythmType = rhythmType
        self.__rhythmDescription = rhythmDescription
        self.__rhythmPattern = rhythmPattern
        self.__timeSignature = timeSignature
        self.__articulation = articulation

    def serialize(self):
        return {
            "rhythmId": self.__rhythmPatternId,
            "rhythmType": self.__rhythmType,
            "rhythmDescription": self.__rhythmDescription,
            "rhythmPattern": self.__rhythmPattern,
            "timeSignature": self.__timeSignature,
            "articulation": self.__articulation,
            "noteLength": self.noteLength,
        }

    @property
    def getRhythmPatternId(self):
        return self.__rhythmPatternId

    @property
    def getRhythmPattern(self):
        return self.__rhythmPattern

    @property
    def getRhythmDescription(self):
        return self.__rhythmDescription

    @property
    def getTimeSignature(self):
        return self.__timeSignature

    @property
    def getRhythmType(self):
        return self.__rhythmType

    @property
    def getArticulation(self):
        return self.__articulation

    @property
    def noteLength(self):
        count = 0
        for r in self.__rhythmPattern:
            for n in r:
                if n.isdigit():
                    count += 1
        n = sum(sublist.count("~") for sublist in self.__rhythmPattern)
        count -= n
        return count

    def __str__(self):
        if self.__rhythmType == "tone":
            string = f" in {self.__timeSignature[0]} / {self.__timeSignature[1]}"
        else:
            string = f"{self.__rhythmDescription} rhythm, in {self.__timeSignature[0]} / {self.__timeSignature[1]}"
        if self.__articulation is not None:
            # TODO Include articulation with nameing
            # string += f" with {self.__articulation.get('name')}."
            pass
        return string
