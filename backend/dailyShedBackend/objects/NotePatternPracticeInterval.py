from objects.PracticeInterval import PracticeInterval
from util.exerciseBucket import dropItInTheBucket
from objects.Scale import Scale
from queries.queries import insertNewRhythmPattern
import random
import abjad
import os

#  FIXME RANGE
class NotePatternPracticeInterval(PracticeInterval):
    def __init__(self,
                 tonic,
                 mode,
                 primaryCollectionTitle,
                 rhythmCollectionTitle,
                 currentIndex,
                 userProgramID,
                 primaryCollectionType,
                 primaryCollectionID,
                 rhythmCollectionID,
                 collectionLength,
                 reviewExercise,
                 instrument,
                 scaleTonicSequence,
                 scalePatternType):
        super().__init__(tonic,
                         mode,
                         primaryCollectionTitle,
                         rhythmCollectionTitle,
                         currentIndex,
                         userProgramID,
                         primaryCollectionType,
                         primaryCollectionID,
                         rhythmCollectionID,
                         collectionLength,
                         reviewExercise,
                         instrument,
                         scaleTonicSequence)
        self.__scalePatternType = scalePatternType
        self.__scale = Scale(tonic, mode, instrument.lowNote, instrument.highNote)
        # self.__scaleExercise = None

    def toDict(self):
        exerciseDict = super().toDict()
        exerciseDict.update({
            "scalePatternType": self.scalePatternType,
            "scale": self.scale.toDict() if hasattr(self.scale, 'toDict') else self.scale,
            # "scaleExercise": self.__scaleExercise.to_dict() if self.__scaleExercise and hasattr(self.__scaleExercise,
            #                                                                                     'to_dict') else self.__scaleExercise
        })
        return exerciseDict

    @property
    def scalePatternType(self):
        return self.__scalePatternType

    @scalePatternType.setter
    def scalePatternType(self, scaleType):
        self.__scalePatternType = scaleType

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        self.__scale = scale

    def findTwoSum(self, nums, target):
        seen = {}
        for num in nums:
            complement = target - num
            if complement in seen:
                return (complement, num)
            seen[num] = True
        return None

    def findRepeatedSum(self, nums, target):
        nums.sort(reverse=True)
        for repeated_num in nums:
            j = 1
            while repeated_num * j < target:
                remainder = target - repeated_num * j
                if remainder in nums and remainder != repeated_num:
                    return (repeated_num, remainder)
                j += 1
        return None

    def multipleBarRhythm(self):
        rhythmCollection = self.getRhythmCollection()
        rhythms = rhythmCollection.get('patterns')
        length = len(self.notePattern)
        # length = len(self.notePattern) if not self.holdLastNote else len(self.notePattern) - 1
        # length = self.getNotePatternRhythmLength()
        measureLength = 0
        remainder = length
        r = []
        subRhythms = []
        rLength = 0
        articulations = []
        lengths = [x.get('rhythmLength') for x in rhythms]
        # possibleRhythms = [x for x in rhythms if remainder % x.get('rhythmLength') == 0]  or None
        repeatedLength, finalLength = self.findRepeatedSum(lengths, length)
        possibleRhythms = [x for x in rhythms if x.get('rhythmLength') == repeatedLength]
        measure = random.choice(possibleRhythms)
        lastMeasure = random.choice([x for x in rhythms if x.get('rhythmLength') == finalLength])
        # lastMeasure = None
        finalLength = 0
        # if not possibleRhythms:
        #     repeatedLength, finalLength = self.findRepeatedSum(lengths, length)
        #     possibleRhythms =  [x for x in rhythms if x.get('rhythmLength') == repeatedLength]
        #     lastMeasure = random.choice([x for x in rhythms if x.get('rhythmLength') == finalLength])

        nextRemainder = remainder - measure.get('rhythmLength')
        subRhythms.append(measure.get('rhythmPatternID'))
        while nextRemainder >= finalLength:
            measureLength += 1
            r.extend(measure.get('rhythmPattern'))
            rLength += measure.get('rhythmLength')
            remainder -= measure.get('rhythmLength')
            if measure.get('articulation'):
                articulations.extend(measure.get('articulation'))
            nextRemainder -= measure.get('rhythmLength')
        if lastMeasure:
            r.extend(lastMeasure.get('rhythmPattern'))
            measureLength += 1
        else:
            r.extend(measure)
            measureLength += 1
            # lastMeasure = measure
        subRhythms.append(lastMeasure.get('rhythmPatternID'))
        rLength += lastMeasure.get('rhythmLength')
        if lastMeasure.get('articulation'):
            articulations.extend(lastMeasure.get('articulation'))
        rhythmDescription = 'multi-measure pattern'
        timeSignature = lastMeasure.get('timeSignature')
        # FIXME: Bring back the insert to DB
        self.rhythmPatternID = insertNewRhythmPattern(
            rhythmCollection.get('collectionID'),
            rhythmDescription,
            articulations,
            timeSignature,
            r,
            rLength,
            subRhythms,
            measureLength
            )
        self.rhythmPattern = r
        self.timeSignature = timeSignature
        self.articulation = articulations

    def selectRandomRhythmPattern(self):
        rhythms = self.getRhythmCollection().get('patterns')
        notePatternLength = self.getNotePatternRhythmLength()

        # For one bar rhythms
        matchingRhythms = [pattern for pattern in rhythms
                           if pattern.get('rhythmLength') == notePatternLength
                           and pattern.get('measureLength') == 1
                           ]
        # Create longer rhythms
        if not matchingRhythms:
            self.multipleBarRhythm()
        else:
            self.rhythmPatternDetails = random.choice(matchingRhythms)

    def getNamedNoteSequence(self):
        ''' Creates a notePattern of abjad named notes.'''
        match self.scalePatternType:
            case 'full_range':
                self.scale.fullRangeAscendingScale()
            case 'one_octave':
                self.scale.oneOctaveAscendingDescendingScale()
            case 'two_octave':
                self.scale.twoOctaveAscendingDescendingScale()
            case 'scale_to_the_ninth':
                self.scale.notePattern = self.notePattern
                self.scale.scaleToTheNinth()
            case _:
                self.scale.notePattern = self.notePattern
                self.scale.defaultScaleExercise()
        self.notePattern = self.scale.notePattern

    def setKey(self):
        if self.currentIndex == self.collectionLength:
            self.incrementTonic()

    def selectExercise(self, collections, notePatternHistory):
        self.collections = collections
        self.notePatternHistory = notePatternHistory
        if not self.reviewExercise or self.currentIndex < 1 and self.currentIndex < self.collectionLength:
            self.incrementMe = self.userProgramID
            self.incrementCurrentIndex()
            self.setKey()
            self.getNotePattern()
            self.getNamedNoteSequence()
        else:
            self.setKey()
            self.getReviewNotePattern()
            self.getNamedNoteSequence()
        if self.rhythmCollectionID:
            self.selectRandomRhythmPattern()

    def createRepeatPhrase(self, notes, scaleNotes=None):
        repeatPhrase = abjad.Container()
        for note in notes:
            if isinstance(note, abjad.Note) or isinstance(note, abjad.Rest):
                repeatPhrase.append(note)
            # FIXME: elif may be unnecessary
            elif note[0][0] == "r" and note[0] != "repeat":
                rest = abjad.Rest(note[0])
                repeatPhrase.append(rest)
        repeat = abjad.Repeat()
        abjad.attach(repeat, repeatPhrase)
        return repeatPhrase

    def createNotePhrase(self, note, scaleNotes = None):
        container = abjad.Container("")
        if isinstance(note[0], list):
            for i, n in enumerate(note):
                if isinstance(n[0], int):
                    container.append(self.numberToNote(scaleNotes, n))
                elif n[0] == '~':
                    tie = abjad.Tie()
                    abjad.attach(tie, container[i - 1])
                else:
                    container.append(n)
        elif isinstance(note[0], (int)):
            n = self.numberToNote(scaleNotes, note)
            container.append(n)
        elif note[0][0] == "r" and note[0] != "repeat":
            container.append(note[0])
        else:
            pass
        return container

    def addHeldLastNote(self, pattern, note):
        if self.holdLastNote:
            match self.timeSignature:
                case (4, 4):
                    heldNoteRhythm = "1"
                case _:
                    heldNoteRhythm = "1"
            pattern.append(abjad.Note(note, (1, heldNoteRhythm)))
        return pattern

    def notationPattern(self):
        if not self.repeatMe:
            notationPattern = []
        else:
            notationPattern = [["repeat"]]
        notes = self.notePattern
        noteIndex = 0
        # Notes in a tie need to be in the same container!
        for r in self.rhythmPattern:
            if isinstance(r[0], int) or r[0].isnumeric():
                notationPattern.append(abjad.Note(self.notePattern[noteIndex], (1, int(r[0]))))
                noteIndex += 1
            elif r == ["~"]:
                noteIndex -= 1
                tie = abjad.Tie()
                abjad.attach(tie, notationPattern[noteIndex])
                # FIXME: Does the index need ot be incremented again.
            else:
                # FIXME: assumes it's a rest. There may be other things
                notationPattern.append(abjad.Rest((1, int(r[0][1:]))))
        pattern = self.addHeldLastNote([notationPattern], notes[0]) if self.holdLastNote else notationPattern
        return pattern

    def buildScore(self):
        container = abjad.Container("")
        pattern = self.notationPattern()
        for index, group in enumerate(pattern):
            if isinstance(group, list) and any('repeat' in item for item in group):
                p = group
                repeatPhrase = self.createRepeatPhrase(p)
                container.append(repeatPhrase)
            elif isinstance(group, (abjad.Note, abjad.Rest)):
                c = abjad.Container()
                c.append(group)
                container.append(c)
            else:
                #  FIXME these else options are note yet tested.
                if isinstance(group, list):
                    container.append(self.createNotePhrase(group))
                else:
                    container.append(self.createNotePhrase(group))
        if self.articulation:
            for articulation in self.articulation:
                match articulation.get('articulation').lower():
                    case 'fermata':
                        a = abjad.Fermata()
                        abjad.attach(a, container[0][int(articulation.get("index"))])
                    case _:
                        pass
        keySignature = abjad.KeySignature(abjad.NamedPitchClass(self.tonic), abjad.Mode(self.mode))
        if isinstance(container[0], abjad.Note):
            abjad.attach(keySignature, container[0])
        else:
            abjad.attach(keySignature, container[0][0])

        ts = tuple(int(x) for x in self.timeSignature)
        timeSignature = abjad.TimeSignature(ts)
        abjad.attach(timeSignature, container[0][0])

        if not abjad.get.indicators(container[-1], abjad.Repeat):
            bar_line = abjad.BarLine("|.")
            last_leaf = abjad.select.leaf(container[-1], -1)
            if last_leaf is not None:
                abjad.attach(bar_line, last_leaf)
            else:
                print("No suitable leaf for bar line attachment found in the last container.")
        return abjad.Score([container], name="Score")

    def setDetails(self):
        self.exerciseName = f"{self.instrument.level}-{self.instrument.instrumentName}-{self.tonic}-{self.mode}-{self.scalePatternType or None}-{self.currentIndex + 1}_of_{self.collectionLength}"
        self.description = f"{self.tonic.title()} {self.mode.title()} {self.scalePatternType.title().replace('_', ' ')} for {self.instrument.instrumentName} {self.instrument.level}. Pattern {self.currentIndex + 1} of {self.collectionLength}"

    def createImage(self):
        lilypond_file = abjad.LilyPondFile([self.preamble, self.buildScore()])
        if not self.filename:
            self.exerciseName = f"{self.instrument.level}_{self.instrument.instrumentName}_{self.scale.tonic}_{self.scale.mode.replace(' ', '_')}_{self.scalePatternType or None}"
            self.filename = self.exerciseID if self.exerciseID else self.exerciseName
        if not self.description:
            self.description = f"{self.tonic.title()} {self.mode.title()} {self.scalePatternType.title()} Scale for {self.instrument.instrumentName} {self.instrument.level}"
        localPath = self.filename
        abjad.persist.as_png(lilypond_file, localPath, flags="-dcrop", resolution=300)
        png = os.path.join(localPath + ".cropped.png")
        dropItInTheBucket(png, localPath)
        os.remove(png)
        os.remove(os.path.join(localPath + ".ly"))

    def createTestImage(self, id = None):
        lilypond_file = abjad.LilyPondFile([self.preamble, self.buildScore()])
        if not self.filename:
            self.filename = f"{self.instrument.level}_{self.instrument.instrumentName}_{self.scale.tonic}_{self.scale.mode.replace(' ', '_')}_{self.scalePatternType or None}"
            self.exerciseName = self.filename
        if not self.description:
            self.description =  f"{self.tonic.title()} {self.mode.title()} {self.scalePatternType.title()} Scale for {self.instrument.instrumentName} {self.instrument.level}"
        localPath = f"{str(id)}_{self.filename}"
        abjad.persist.as_png(lilypond_file, localPath, flags="-dcrop", resolution=300)
        os.remove(os.path.join(localPath + ".ly"))