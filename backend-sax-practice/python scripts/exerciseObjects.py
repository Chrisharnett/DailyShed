import os
import abjad
import math
import boto3


class Exercise:
    def __init__(
        self,
        exerciseId,
        exerciseFileName,
        noteRhythmPattern,
        description,
        key="g",
        mode="major",
        timeSignature=[4, 4],
        articulation=[],
        dynamics=[],
        preamble=r"#(set-global-staff-size 28)",
    ):
        self.__exerciseId = exerciseId
        self.__exerciseFileName = exerciseFileName
        self.__noteRhythmPattern = noteRhythmPattern
        self.__key = key
        self.__mode = mode
        self.__description = description
        self.__timeSignature = timeSignature
        self.__preamble = preamble
        self.__articulation = articulation
        self.__dynamics = dynamics

    @property
    def buildScore(self):
        container = abjad.Container("")
        scaleNotes = self.getScaleNotes()

        for note in self.__noteRhythmPattern:
            if isinstance(note[0], int):
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
            attachHere = container[0][0]
        if attachHere != "":
            keySignature = abjad.KeySignature(
                abjad.NamedPitchClass(self.__key), abjad.Mode(self.__mode)
            )
            abjad.attach(keySignature, attachHere)
            timeSignature = abjad.TimeSignature(tuple(self.__timeSignature))
            abjad.attach(timeSignature, attachHere)
            if not abjad.get.indicators(container[-1], abjad.Repeat):
                bar_line = abjad.BarLine("|.")
                abjad.attach(bar_line, container[-1])
        if len(self.__articulation) > 0:
            for articulation in self.__articulation:
                if articulation.get("articulation").lower() == "fermata":
                    a = abjad.Fermata()
                    abjad.attach(a, container[articulation.get("index")][0])

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
        n = pitchName + note[1] + " "

        return n

    def path(self):
        return os.path.join("static/img/" + self.exerciseFileName) + ".cropped.png"

    def createImage(self):
        # score = self.buildScore()

        lilypond_file = abjad.LilyPondFile([self.__preamble, self.buildScore])
        localPath = os.path.join("static/img/" + self.__exerciseFileName)
        abjad.persist.as_png(lilypond_file, localPath, flags="-dcrop", resolution=300)

        # os.remove(os.path.join("static/img/" + self.exerciseFileName) + ".ly")

        s3BucketName = "mysaxpracticeexercisebucket"
        png = os.path.join(localPath + ".cropped.png")

        s3_client = boto3.client("s3")
        s3_client.upload_file(png, s3BucketName, self.__exerciseFileName)

        ly = os.path.join(localPath + ".ly")

        os.remove(png)
        os.remove(ly)

        exerciseURL = f"https://mysaxpracticeexercisebucket.s3.amazonaws.com/{self.__exerciseFileName}"

        return exerciseURL


class NotePattern:
    def __init__(
        self,
        patternId,
        patternType,
        notePattern,
        preamble,
        description="",
        timeSignature=(4, 4),
        rhythm="",
        articulation="",
        dynamic="",
        direction="",
    ):
        self.__patternId = patternId
        self.__patternType = patternType
        self.__notePattern = notePattern
        self.__preamble = preamble
        self.__description = description

    @property
    def getPatternId(self):
        return self.__patternId

    @property
    def getPatternType(self):
        return self.__patternType

    @property
    def getNotePattern(self):
        return self.__notePattern

    @property
    def getPreamble(self):
        return self.__preamble

    @property
    def getDescription(self):
        return self.__description

    def __str__(self):
        name = self.__patternType + "_" + str(self.__patternId)
        return name


class Scale:
    def __init__(self, tonic, mode):
        self.__tonic = tonic
        self.__mode = mode

    def getPitches(self):
        pitchSets = {
            "major": [0, 2, 4, 5, 7, 9, 11],
            "natural_minor": [0, 2, 3, 5, 7, 8, 10],
            "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
            "jazz_minor": [0, 2, 3, 5, 7, 9, 11],
        }
        return pitchSets

    def makeScale(self):
        pitches = []
        tonic = abjad.NamedPitch(self.__tonic)
        for scalePitch in self.getPitches()[self.__mode]:
            pitch = tonic + scalePitch
            pitches.append(pitch)
        return pitches


def main():
    exercise = Exercise(
        -1,
        "NA",
        [
            [
                "repeat",
                [1, "4"],
                [2, "4"],
                [3, "4"],
                [4, "4"],
                [5, "4"],
                [6, "4"],
                [7, "4"],
                [8, "4"],
                [9, "4"],
                [8, "4"],
                [7, "4"],
                [6, "4"],
                [5, "4"],
                [4, "4"],
                [3, "4"],
                [2, "4"],
            ],
            [1, "1"],
        ],
        "A description",
        "g",
        "mode",
        [4, 4],
        [],
        [],
        r"#(set-global-staff-size 28)",
    )
    exerciseImage = exercise.createImage()
    print(exerciseImage)


if __name__ == "__main__":
    main()
