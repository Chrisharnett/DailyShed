from objects.NotePattern import (MusicPattern,
                                 LongTone,
                                 ScalePattern)
from objects.RhythmPattern import RhythmPattern
import math
import copy

class PatternCollection:
    def __init__(self, title, collectionType, patterns=None):
        self.__title = title
        self.__collectionType = collectionType
        self.__patterns = patterns if patterns else []
        self.__collectionLength = len(patterns) if patterns else 0

    def __str__(self):
        return self.__title

    @property
    def collectionType(self):
        return self.__collectionType

    @collectionType.setter
    def collectionType(self, value):
        self.__collectionType = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def patterns(self):
        return self.__patterns

    @patterns.setter
    def patterns(self, value):
        self.__patterns = value

    @property
    def collectionLength(self):
        return self.__collectionLength

    @collectionLength.setter
    def collectionLength(self, value):
        self.__collectionLength = value

    def addPattern(self, pattern):
        if isinstance(pattern, MusicPattern):
            self.__patterns.append(pattern)
            self.__collectionLength += 1
        else:
            raise TypeError("Only instances of MusicPatterns or its subclasses can be added.")

    def removePattern(self, pattern):
        if pattern in self.__patterns:
            self.__patterns.remove(pattern)
        else:
            raise ValueError("Pattern not found in collection.")

    def getPatterns(self):
        return self.__patterns

    def findPatternByType(self, patternType):
        return [pattern for pattern in self.__patterns if pattern.patternType == patternType]

class ScalePatternCollection(PatternCollection):
    def __init__(self, mode, scalePatternType):
        id = 0
        collectionType = 'notePattern'
        collectionName = 'scale_exercise'
        title = f"{mode.get('modeName')},{collectionName}"
        super().__init__(title, collectionType)
        self.mode = mode
        self.__scalePatternType = scalePatternType
        notePattern = mode.get('modePattern')
        description = f"{title.title().replace('_', ' ')}. Play twice. Repeat both times."
        self.addPattern(ScalePattern(title, notePattern, description, scalePatternType, patternID=str(id)))
        id += 1

class ScaleToTheNinthBuilderCollection(PatternCollection):
    def __init__(self, mode):
        collectionType = 'notePattern'
        title = f"{mode.get('modeName')},scale_to_the_ninth"
        super().__init__(title, collectionType)
        self.__mode = mode
        directions = ['ascending', 'descending', 'ascending/descending', 'descending/ascending']
        holdLastNote = True
        repeatMe = True
        modePattern = mode.get('modePattern')
        topNote = modePattern[0]+12
        ninth = modePattern[1]+12
        modePattern.append(topNote)
        modePattern.append(ninth)
        notePatterns = self.createPatternLists(modePattern)
        for pattern in notePatterns:
            id = 0
            #  FIXME
            description = f"{title.title().replace('_', ' ')}. Play twice. Repeat both times."
            self.addPattern(ScalePattern(f"{title}", pattern, description, 'scale_to_the_ninth', directions,
                                      holdLastNote=holdLastNote, repeatMe=repeatMe, patternID=str(id)))
            id += 1

    def createPatternLists(self, elements):
        if not elements:
            return []

        result = []
        n = len(elements)

        def generateSublist(start, end, step):
            sublist = []
            for i in range(start, end, step):
                sublist.append(elements[i % n])
            return sublist

        for i in range(2, n + 1):
            # Ascending pattern
            ascending = generateSublist(0, i, 1)
            if ascending not in result:
                result.append(ascending)

            # Descending pattern
            descending = generateSublist(i - 1, -1, -1)
            if descending not in result:
                result.append(descending)

            # Ascending-Descending pattern
            ascDesc = generateSublist(0, i, 1) + generateSublist(i - 2, -1, -1)
            if ascDesc not in result:
                result.append(ascDesc)

            # Descending-Ascending pattern
            descAsc = generateSublist(i - 1, -1, -1) + generateSublist(1, i, 1)
            if descAsc not in result:
                result.append(descAsc)

        return result

class SingleNoteDiatonicLongToneCollection(PatternCollection):
    def __init__(self, mode):
        id = 0
        collectionType = 'notePattern'
        title = f"{mode.get('modeName')},single_note_long_tone"
        super().__init__(title, collectionType)

        self.__mode = mode

        directions = ['static']
        holdLastNote = False
        repeatMe = False
        modePattern = mode.get('modePattern')

        singleNoteLongToneCollections = []
        for note in modePattern:
            id = 0
            #  FIXME
            description = f"{title.title().replace('_', ' ')}. Play twice. Internalize the sound you create."
            self.addPattern(LongTone(collectionType, [note], description, directions,
                                      holdLastNote=holdLastNote, repeatMe=repeatMe, patternID=str(id)))
            id += 1

class RhythmCollection(PatternCollection):
    def __init__(self, title, collectionType, timeSignature=(4,4)):
        super().__init__(title, collectionType)
        self.__timeSignature = timeSignature

    def fillBar(self, element, numerator):
        bar = []
        elementString = str(element)
        for i in range(numerator):
            if (elementString[0] == 'r'):
                rhythm = int(elementString[1:])
            else:
                rhythm = int(elementString)
            for j in range(math.floor(rhythm / numerator)):
                bar.append([elementString])
        return bar

    def noDuplicateRhythms(self, newPattern):
        for pattern in self.patterns:
            if pattern.pattern == newPattern:
                return False
        return True

class SingleNoteLongToneRhythms(RhythmCollection):
    def __init__(self, timeSignature):
        collectionType='long_tone_rhythm'
        title='single_note_long_tone_rhythms'
        match timeSignature:
            case (4, 4):
                rhythm = "1"
                title += "_in_4-4"
            case _:
                rhythm = "1"
                title += "_in_4-4"
        super().__init__(title, collectionType, timeSignature)

        id = 0

        noteRhythm = [rhythm]
        pattern = [noteRhythm]
        measureLength = 1
        description = title[:-1] + 'with fermata'
        articulation = [{"articulation": "fermata", "index": 0, "name": "fermata"}]
        self.addPattern(RhythmPattern(collectionType,
                                    pattern,
                                    description,
                                    timeSignature,
                                    articulation,
                                    measureLength,
                                    patternID=str(id)))
        id += 1

        pattern = [noteRhythm, ["~"], noteRhythm]
        description = f"{title[:-1].title().replace('_', ' ')}.Hold 2 measures."
        articulation = None
        measureLength = 2
        self.addPattern(RhythmPattern(collectionType,
                                      pattern,
                                      description,
                                      timeSignature,
                                      articulation,
                                      measureLength,
                                      patternID=str(id)))

class QuarterNoteAndRestCollection(RhythmCollection):
    def __init__(self, timeSignature):
        title = 'quarter_note'
        collectionType = 'rhythm'
        match timeSignature:
            case (4, 4):
                title += "_in_4-4"
            case _:
                title += ""
        super().__init__(title, collectionType, timeSignature)

        id = 0
        rhythmPatterns = []
        rest = 'r4'
        bar = self.fillBar(timeSignature[1], timeSignature[0])
        description = 'Full bar of quarters'
        articulation = None
        measureLength = 1
        self.addPattern(RhythmPattern(collectionType,
                                      bar,
                                      description,
                                      timeSignature,
                                      articulation,
                                      measureLength,
                                      patternID=str(id)))
        id += 1

        for i in range(timeSignature[0]):
            quarterAndRestRhythms = copy.deepcopy(bar)
            for j, note in enumerate(bar):
                quarterAndRestRhythms[j][0] = rest

            quarterAndRestRhythms[i] = [timeSignature[1]]
            if self.noDuplicateRhythms(quarterAndRestRhythms):
                description = "One quarter, 3 rests"
                self.addPattern(RhythmPattern(collectionType,
                                              quarterAndRestRhythms,
                                              description,
                                              timeSignature,
                                              articulation,
                                              measureLength,
                                              patternID=str(id)))
                id += 1

        for i in range(timeSignature[0]):
            for j in range(1 + i, timeSignature[0]):
                quarterAndRestRhythms = self.fillBar(rest, timeSignature[0])
                quarterAndRestRhythms[i] = [timeSignature[1]]
                quarterAndRestRhythms[j] = [timeSignature[1]]
                description = '2 quarters, 2 rests'
                if self.noDuplicateRhythms(quarterAndRestRhythms) == True:
                    self.addPattern(RhythmPattern(collectionType,
                                                  quarterAndRestRhythms,
                                                  description,
                                                  timeSignature,
                                                  articulation,
                                                  measureLength,
                                                  patternID=str(id)))
                    id += 1

        oppositePatterns = []
        for bar in self.patterns[1:]:
            newPattern = []
            p = bar.pattern
            for r in p:
                if r == [timeSignature[1]]:
                    newPattern.append([rest])
                elif r == [rest]:
                    newPattern.append([timeSignature[1]])
            oppositePatterns.append(newPattern)

        description = '3 quarters, 1 rest'
        for newPattern in oppositePatterns:
            if self.noDuplicateRhythms(newPattern):
                self.addPattern(RhythmPattern(collectionType,
                                              newPattern,
                                              description,
                                              timeSignature,
                                              articulation,
                                              measureLength,
                                              patternID=str(id)))
                id += 1

class EighthAndQuarterRhythms(RhythmCollection):
    def __init__(self, timeSignature):
        title = 'eighth_and_quarter_note_rhythms'
        collectionType = 'rhythm'
        match timeSignature:
            case (4, 4):
                title += "_in_4-4"
            case _:
                title += ""
        super().__init__(title, collectionType, timeSignature)

        numerator = timeSignature[0]
        denominator = timeSignature[1]
        id = 0
        rhythmPatterns = []
        division = int(8 / int(denominator))

        oneBarOfBeats = self.fillBar(denominator, numerator)
        eighthAndRest = ['8', 'r8']
        # all combinations of beats and 1 beat of eighths
        description = title
        articulation = None
        measureLength = 1
        for i, beat in enumerate(oneBarOfBeats):
            for r in eighthAndRest:
                newRhythm = oneBarOfBeats.copy()
                newRhythm[i] = [r]
                for j in range(division - 1):
                    newRhythm.insert(j + i + 1, ['8'])
                if self.noDuplicateRhythms(newRhythm):
                    self.addPattern(RhythmPattern(collectionType,
                                                  newRhythm,
                                                  description,
                                                  timeSignature,
                                                  articulation,
                                                  measureLength,
                                                  patternID=str(id)))
                    id += 1
                if division != 1:
                    for k, beat in enumerate(oneBarOfBeats):
                        newIndex = (k + division + i)
                        if newIndex <= len(oneBarOfBeats):
                            twoEighthPairs = newRhythm.copy()
                            twoEighthPairs[newIndex] = ['8']
                            for j in range(division - 1):
                                twoEighthPairs.insert(newIndex + 1, ['8'])
                                description = '2 eighth pairs'
                            if self.noDuplicateRhythms(twoEighthPairs):
                                self.addPattern(RhythmPattern(collectionType,
                                                              twoEighthPairs,
                                                              description,
                                                              timeSignature,
                                                              articulation,
                                                              measureLength,
                                                              patternID=str(id)))
                                id += 1
        oneBarOfEights = self.fillBar('8', numerator)
        description = 'One bar of eighths'
        self.addPattern(RhythmPattern(collectionType,
                                      oneBarOfEights,
                                      description,
                                      timeSignature,
                                      articulation,
                                      measureLength,
                                      patternID=str(id)))

        for i, eighth in enumerate(oneBarOfEights):
            if i % 2 == 0:
                newRhythm = oneBarOfEights.copy()
                newRhythm[i] = ['r8']
                description = 'Bar of eighths with one eighth rest.'
                self.addPattern(RhythmPattern(collectionType,
                                              newRhythm,
                                              description,
                                              timeSignature,
                                              articulation,
                                              measureLength,
                                              patternID=str(id)))
                id += 1
