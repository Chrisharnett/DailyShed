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
    ):
        self.__pitchPattern = pitchPattern
        self.__rhythmPattern = rhythmPattern
        self.__key = key
        self.__mode = mode
        self.__preamble = preamble
    def serialize(self):
        return {"exerciseName": self.exerciseFileName(),
                "pitchPattern": self.__pitchPattern.serialize(),
                "rhythmPattern": self.__rhythmPattern.serialize(),
                "key": self.__key,
                "mode": self.__mode,
                "imageFileName": self.exerciseFileName() + ".cropped.png",
                "imageURL": self.imageURL(),
                "description": str(self)
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
        notationPattern = []
        rhythms = self.__rhythmPattern.getRhythmPattern
        notes = self.__pitchPattern.getNotePattern
        # Use the same note before and after a tie by adding to the notePattern
        # for i in range(len(self.__rhythmPattern.getRhythmPattern)):
        #     if self.__rhythmPattern.getRhythmPattern[i] == ['~']:
        #         self.__pitchPattern.getNotePattern.insert(self.__pitchPattern.getNotePattern[i + 1], i)
        noteIndex = 0
        for r in rhythms:
            if r[0].isnumeric():
                notationPattern.append([notes[noteIndex], r[0]])
                noteIndex += 1
            elif r == ['~']:
                noteIndex -= 1
            else:
                notationPattern.append(r)
            # if (self.__rhythmPattern.getRhythmPattern[k][0]).isnumeric():
            #     note = [self.__pitchPattern.getNotePattern[k], self.__rhythmPattern.getRhythmPattern[k][0]]
            #     notationPattern.append(note)
        return notationPattern

    def exerciseFileName(self):
        return f"{self.__key}_{self.__mode}_{str(self.__pitchPattern.getPatternId)}_{str(self.__rhythmPattern.getRhythmPatternId)}"

    def imageURL(self):
        return f"https://mysaxpracticeexercisebucket.s3.amazonaws.com/{self.exerciseFileName()}"

    @property
    def buildScore(self):
        container = abjad.Container("")
        scaleNotes = self.getScaleNotes()
        pattern = self.notationPattern()
        for note in pattern:
            if isinstance(note[0], int):
                n=self.numberToNote(scaleNotes, note)
                container.append(self.numberToNote(scaleNotes, note))
            elif note[0] == "r":
                container.append(note)
            elif note[0] == "repeat":
                notes = ""
                for n in note[1:]:
                    if isinstance(n[0], int):
                        notes += self.numberToNote(scaleNotes, n)
                    else:
                        notes += n[0]
                c = abjad.Container(notes)
                r = abjad.Repeat()
                abjad.attach(r, c)
                container.append(c)
        attachHere = ""
        if len(container) >= 1:
            attachHere = container[0]
            # attachHere = container[0][0]
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
                abjad.attach(bar_line, container[-1])
        if self.__rhythmPattern.getArticulation:
            for articulation in self.__rhythmPattern.getArticulation:
                if articulation.get("articulation").lower() == "fermata":
                    a = abjad.Fermata()
                    abjad.attach(a, container[articulation.get("index")])

        voice = abjad.Voice([container], name="Exercise_Voice")
        staff = abjad.Staff([voice], name="Exercise_Staff")
        score = abjad.Score([staff], name="Score")
        return score

    def getScaleNotes(self):
        scale = Scale(self.__key + "'", self.__mode)
        scaleNotes = scale.makeScale()
        return scaleNotes

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

    def path(self):
        return os.path.join("static/img/" + self.__str__()) + ".cropped.png"


    def createImage(self):
        # score = self.buildScore()
        lilypond_file = abjad.LilyPondFile([self.__preamble, self.buildScore])
        #  It only works with absolute path here, but still places files in root instead of /temp
        absolutePath = "/Users/christopherharnett/Library/CloudStorage/OneDrive-CollegeoftheNorthAtlantic/Documents/Software Development/ASD/Fall/Capstone 3540/reactSaxPracticeApp/backend-sax-practice/python scripts/temp/"
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

class Collection:
    def __init__(self, name):
        self.__name = name
        self.__patterns = []

    def __str__(self):
        return self.__name

    def __iter__(self):
        return iter(self.__patterns)

    @property
    def getName(self):
        return self.__name

    @property
    def getPatterns(self):
        return self.__patterns

    def addPattern(self, pattern):
        self.__patterns.append(pattern)

class NotePattern:
    def __init__(
        self,
        notePatternId,
        notePatternType,
        notePattern,
        rhythmMatcher='general',
        description="",
        dynamic="",
        direction=""
    ):
        self.__patternId = notePatternId
        self.__notePatternType = notePatternType
        self.__notePattern = notePattern
        self.__rhythmMatcher = rhythmMatcher
        self.__description = description
        self.__dynamic = dynamic
        self.__direction = direction

    def serialize(self):
        return{"notePatternId": self.__patternId,
               "notePatternType": self.__notePatternType,
               "notePattern": self.__notePattern,
               "rhythmMatcher": self.__rhythmMatcher,
               "description": self.__description,
               "dynamic": self.__dynamic,
               "direction": self.__direction}

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
    def __init__(self, rhythmPatternId, rhythmType, rhythmDescription, rhythmPattern, timeSignature, articulation = None):
        self.__rhythmPatternId = rhythmPatternId
        self.__rhythmType = rhythmType
        self.__rhythmDescription = rhythmDescription
        self.__rhythmPattern = rhythmPattern
        self.__timeSignature = timeSignature
        self.__articulation = articulation

    def serialize(self):
        return {"rhythmId": self.__rhythmPatternId,
                "rhythmType": self.__rhythmType,
                "rhythmDescription": self.__rhythmDescription,
                "rhythmPattern": self.__rhythmPattern,
                "timeSignature": self.__timeSignature,
                "articulation": self.__articulation,
                "noteLength": self.noteLength}
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
        if self.__rhythmType == 'tone':
            string = f" in {self.__timeSignature[0]} / {self.__timeSignature[1]}"
        else:
            string = f"{self.__rhythmDescription} rhythm, in {self.__timeSignature[0]} / {self.__timeSignature[1]}"
        if self.__articulation is not None:
            # TODO Include articulation with nameing
            # string += f" with {self.__articulation.get('name')}."
            pass
        return string


