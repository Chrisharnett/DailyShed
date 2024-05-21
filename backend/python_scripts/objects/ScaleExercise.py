import abjad
import random
from objects.Exercise import Exercise

class ScaleExercise(Exercise):
    def __init__(self, scale):
        super().__init__(scale.tonic, scale.mode, notePattern=scale.pattern, holdLastNote=True, repeatMe=True)
        self.__scale = scale

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
        for i in range(len(nums)):
            repeated_num = nums[i]
            j = 1
            while repeated_num * j < target:
                remainder = target - repeated_num * j
                if remainder in nums and remainder != repeated_num:
                    return (repeated_num, remainder)
                j += 1
        return None

    def multipleBarRhythm(self, rhythms):
        length = len(self.notePattern)
        remainder = length
        r = []
        id = []
        rLength = 0
        artic = []
        lengths = [r.get('rhythmLength') for r in rhythms]
        possibleRhythms = [x for x in rhythms if remainder % x.get('rhythmLength') == 0]  or None
        lastMeasure = None
        finalLength =0
        if not possibleRhythms:
            repeatedLength, finalLength = self.findRepeatedSum(lengths, length)
            possibleRhythms =  [x for x in rhythms if x.get('rhythmLength') == repeatedLength]
            lastMeasure = random.choice([x for x in rhythms if x.get('rhythmLength') == finalLength])
        measure = random.choice(possibleRhythms)
        nextRemainder = remainder - measure.get('rhythmLength')
        id.append(f"-{str(measure.get('rhythmPatternID'))}")
        while nextRemainder >= finalLength:
            r.extend(measure.get('rhythmPattern'))
            rLength += measure.get('rhythmLength')
            remainder -= measure.get('rhythmLength')
            if measure.get('articulation'):
                artic.extend(measure.get('articulation'))
            nextRemainder -= measure.get('rhythmLength')
        if lastMeasure:
            r.extend(lastMeasure.get('rhythmPattern'))
        else:
            lastMeasure = measure
        id.append(f"-{str(lastMeasure.get('rhythmPatternID'))}")
        rLength += lastMeasure.get('rhythmLength')
        if lastMeasure.get('articulation'):
            artic.extend(lastMeasure.get('articulation'))
        rhythmDescription = lastMeasure.get('rhythmDescription')
        timeSignature = lastMeasure.get('timeSignature')
        # FIXME: Bring back the insert to DB
        # rhythmPatternID = insertNewRhythmPattern(
        #     rhythms.get('collectionID'),
        #     rhythmDescription,
        #     artic,
        #     timeSignature,
        #     r,
        #     rLength,
        #     id
        #     )
        self.rhythmPattern = r
        self.timeSignature = timeSignature
        self.articulation = artic
        self.rhythmPatternID = 'test'

    def createRepeatPhrase(self, notes, scaleNotes = None):
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

    def getRandomRhythmPattern(self, rhythms):
        matchingRhythms = [pattern for pattern in rhythms if pattern.get('rhythmLength') == self.getNotePatternRhythmLength()]
        if not matchingRhythms:
            return self.multipleBarRhythm(rhythms)
        else:
            return random.choice(matchingRhythms)

    def addHeldLastNote(self, pattern, note):
        returnPattern = pattern
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
                self.addTie(noteIndex)
                notationPattern.append(r)
                # FIXME: Does the index need ot be incremented again.
            else:
                # FIXME: assumes it's a rest. There may be other things
                notationPattern.append(abjad.Rest((1, int(r[0][1:]))))

        pattern = self.addHeldLastNote([notationPattern], notes[0]) if self.holdLastNote else None
        # heldNoteRhythm = None
        # if self.holdLastNote:
        #     match self.timeSignature:
        #         case (4,4):
        #             heldNoteRhythm = "1"
        #         case _:
        #             pass
        #     pattern.append(abjad.Note(notes[-1], (1, heldNoteRhythm)))
        return pattern

    def buildScore(self):
        # rhythms = eighthAndQuarterRhythms(int(4), '4')
        # rhythms = quarterNoteAndRestRhythms(int(4), '4')
        # self.getRandomRhythmPattern(rhythms)
        container = abjad.Container("")
        pattern = self.notationPattern()
        for index, group in enumerate(pattern):
            if isinstance(group, list) and any('repeat' in item for item in group):
                p = group
                repeatPhrase = self.createRepeatPhrase(p)
                container.append(repeatPhrase)
            elif isinstance(group, (abjad.Note, abjad.Rest)):
                container.append(group)
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
