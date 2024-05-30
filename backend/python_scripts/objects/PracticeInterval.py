import random
from queries.queries import insertNewRhythmPattern
from objects.Exercise import Exercise

class PracticeInterval(Exercise):
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
                 scaleTonicSequence = None):
        super().__init__(tonic = tonic, mode = mode)
        # self.__interval = interval
        self.__primaryCollectionTitle = primaryCollectionTitle
        self.__rhythmCollectionTitle = rhythmCollectionTitle
        self.__currentIndex = currentIndex
        self.__userProgramID = userProgramID
        self.__primaryCollectionType = primaryCollectionType
        self.__primaryCollectionID = primaryCollectionID
        self.__rhythmCollectionID = rhythmCollectionID
        self.__collectionLength = collectionLength
        self.__reviewExercise = reviewExercise
        self.__instrument = instrument
        self.__directions = None
        self.__notePatternDetails = {}
        self.__rhythmPatternDetails = {}
        self.__incrementMe = False
        self.__collections = None
        self.__notePatternHistory = None
        self.__scaleTonicSequence = scaleTonicSequence

    @property
    def instrument(self):
        return self.__instrument

    @instrument.setter
    def instrument(self, instrument):
        self.__instrument = instrument

    @property
    def scaleTonicSequence(self):
        return self.__scaleTonicSequence

    @scaleTonicSequence.setter
    def scaleTonicSequence(self, sequence):
        self.__scaleTonicSequence = sequence

    def incrementTonic(self):
        newTonic = self.scaleTonicSequence[self.scaleTonicSequence.index(self.tonic) +1 ]
        self.tonic = newTonic
    #     TODO: call to update scaleTonicIndex in DB

    def incrementScaleTonicIndex(self):
        index = self.scaleTonicSequence.index(self.tonic)
        return index + 1

    def getCurrentKey(self):
        return self.scaleTonicSequence[self.__scaleTonicIndex]

    @property
    def directions(self):
        return self.__directions

    @directions.setter
    def directions(self, directions):
        self.__directions = directions

    @property
    def primaryCollectionTitle(self):
        return self.__primaryCollectionTitle

    @primaryCollectionTitle.setter
    def primaryCollectionTitle(self, title):
        self.__primaryCollectionTitle = title

    @property
    def rhythmCollectionTitle(self):
        return self.__rhythmCollectionTitle

    @rhythmCollectionTitle.setter
    def rhythmCollectionTitle(self, rhythmCollectionTitle):
        self.__rhythmCollectionTitle = rhythmCollectionTitle

    @property
    def currentIndex(self):
        return self.__currentIndex

    @currentIndex.setter
    def currentIndex(self, index):
        self.__currentIndex = index

    def incrementCurrentIndex(self):
        newIndex = self.currentIndex + 1
        self.currentIndex = newIndex
        self.incrementMe = self.userProgramID

    @property
    def userProgramID(self):
        return self.__userProgramID

    @userProgramID.setter
    def userProgramID(self, id):
        self.__userProgramID = id

    @property
    def primaryCollectionType(self):
        return self.__primaryCollectionType

    @primaryCollectionType.setter
    def primaryCollectionType(self, type):
        self.__primaryCollectionType = type

    @property
    def primaryCollectionID(self):
        return self.__primaryCollectionID

    @primaryCollectionID.setter
    def primaryCollectionID(self, id):
        self.__primaryCollectionID = id

    @property
    def rhythmCollectionID(self):
        return self.__rhythmCollectionID

    @rhythmCollectionID.setter
    def rhythmCollectionID(self, id):
        self.__rhythmCollectionID = id

    @property
    def collectionLength(self):
        return self.__collectionLength

    @collectionLength.setter
    def collectionLength(self, length):
        self.__collectionLength = length

    @property
    def reviewExercise(self):
        return self.__reviewExercise

    @reviewExercise.setter
    def reviewExercise(self, boolean):
        self.__reviewExercise = boolean

    @property
    def rhythmPatternDetails(self):
        return self.__rhythmPatternDetails

    @rhythmPatternDetails.setter
    def rhythmPatternDetails(self, rhythmPatternDetails):
        self.rhythmPatternID = rhythmPatternDetails.get('rhythmPatternID')
        self.rhythmPattern = rhythmPatternDetails.get('rhythmPattern')
        self.articulation = rhythmPatternDetails.get('articulation')
        self.timeSignature = rhythmPatternDetails.get('timeSignature')
        self.__rhythmPatternDetails = rhythmPatternDetails

    @property
    def notePatternDetails(self):
        return self.__notePatternDetails

    @notePatternDetails.setter
    def notePatternDetails(self, notePatternDetails):
        self.notePatternID = notePatternDetails.get('notePatternID')
        self.notePattern = notePatternDetails.get('notePattern')
        self.directionIndex = notePatternDetails.get('currentDirectionIndex')
        self.directions = notePatternDetails.get('directions')
        self.holdLastNote = notePatternDetails.get('holdLastNote')
        self.repeatMe = notePatternDetails.get('repeatMe')
        self.__notePatternDetails = notePatternDetails

    @property
    def incrementMe(self):
        return self.__incrementMe

    @incrementMe.setter
    def incrementMe(self, userProgramID):
        self.__incrementMe = userProgramID

    @property
    def noteLength(self):
        return self.__notePatternDetails.get('noteLength')

    @noteLength.setter
    def noteLength(self, length):
        self.__notePatternDetails['noteLength'] = length

    @property
    def collections(self):
        return self.__collections

    @collections.setter
    def collections(self, collections):
        self.__collections = collections

    @property
    def notePatternHistory(self):
        return self.__notePatternHistory

    @notePatternHistory.setter
    def notePatternHistory(self, history):
        self.__notePatternHistory = history

    @property
    def rhythmDescription(self):
        return self.__rhythmPatternDetails.get('rhythmDescription')

    def getExerciseDetails(self):
        pass

    def determineDirection(self):
        currentDirectionIndex = self.directionIndex
        directions = self.directions
        if not currentDirectionIndex:
            self.directionIndex = 0
        elif currentDirectionIndex < len(directions):
            newIndex = currentDirectionIndex + 1
            self.directionIndex = newIndex
        elif currentDirectionIndex == 'r' or currentDirectionIndex == (len(directions) -1):
            validDirectionIndices =[i for i in range(len(directions)) if i != self.directionIndex]
            self.directionIndex = random.choice(validDirectionIndices)
        self.applyNewDirection()

    def applyNewDirection(self):
        direction = self.directions[int(self.directionIndex)]
        match direction:
            case 'ascending':
                return
            case 'descending':
                self.descendingPattern()
            case 'ascending/descending':
                self.ascendingDescendingPattern()
            case 'descending/ascending':
                self.descendingAscendingPattern()
            case _:
                return

    def descendingPattern(self):
        d = self.notePattern.copy()
        d.reverse()
        self.notePattern = d
        self.newNoteLength()

    def ascendingDescendingPattern(self):
        a = self.notePattern.copy()
        d = self.notePattern.copy()
        d.reverse()
        a.pop()
        a.extend(d)
        self.notePattern = a
        self.newNoteLength()

    def descendingAscendingPattern(self):
        d = self.notePattern.copy()
        d.reverse()
        d.pop()
        d.extend(self.notePattern)
        self.notePattern = d
        self.newNoteLength()

    def newNoteLength(self):
        newLength = self.getNotePatternRhythmLength()
        self.noteLength = newLength

    def getNotePattern(self):
        for collection in self.collections:
            if collection.get('collectionID') == self.primaryCollectionID:
                notePatternDetails = collection.get('patterns')[self.currentIndex % len(collection.get('patterns'))]
                self.notePatternDetails = notePatternDetails
        return None

    def minPlayCount(self, patterns):
        return min(pattern['playcount'] for pattern in patterns)

    def getReviewNotePattern(self):
        min = self.minPlayCount(self.notePatternHistory)
        reviewPatterns = [pattern for pattern in self.notePatternHistory if pattern.get('playcount') == min]
        notePatternID  = random.choice(reviewPatterns).get('notePatternID')
        directionIndex = next(pattern.get('directionIndex') for pattern in self.notePatternHistory if pattern.get('notePatternID') == notePatternID)
        coll = next(collection for collection in self.collections if collection.get('collectionID') == self.primaryCollectionID)
        notePattern = next(pattern for pattern in coll.get('patterns') if pattern.get('notePatternID') == notePatternID)
        if directionIndex:
            notePattern['currentDirectionIndex'] = (directionIndex + 1) % len(notePattern.get('directions'))
        self.notePatternDetails = notePattern

    def maxRhythmNoteLength(self, rhythms):
        return max(rhythms.get('patterns'), key=lambda x: x.get('rhythmLength')).get('rhythmLength')

    def multipleBarRhythm(self):
        rhythms = self.getRhythmCollection()
        length = self.notePatternDetails.get('noteLength')
        # maxRhythmLength = self.maxRhythmNoteLength(rhythms)
        # minimumNumberOfMeasures = math.ceil(length / maxRhythmLength)
        remainder = length
        r = []
        id = []
        rLength = 0
        artic = []
        # TODO: changed placement so a measure is repeated until
        possibleRhythms = [
            x for x in rhythms.get('patterns') if remainder / 2 <= x.get('rhythmLength') <= remainder
        ]
        measure = random.choice(possibleRhythms)
        while remainder >= measure.notelength:
            r.extend(measure.get('rhythmPattern'))
            id.append(f"-{str(measure.get('rhythmPatternID'))}")
            rLength += measure.get('rhythmLength')
            remainder -= measure.get('rhythmLength')
            if measure.get('articulation'):
                artic.extend(measure.get('articulation'))
        possibleRhythms = [x for x in rhythms.get('patterns') if x.get('rhythmLength') == remainder]
        lastMeasure = random.choice(possibleRhythms)
        id.append(f"-{str(measure.get('rhythmPatternID'))}")
        rLength += lastMeasure.get('rhythmLength')
        if lastMeasure.get('articulation'):
            artic.extend(lastMeasure.get('articulation'))
        r.extend(lastMeasure.get('rhythmPattern'))
        # random.shuffle(r)
        rhythmDescription = lastMeasure.get('rhythmDescription')
        timeSignature = lastMeasure.get('timeSignature')
        rhythmPatternID = insertNewRhythmPattern(
            rhythms.get('collectionID'),
            rhythmDescription,
            artic,
            timeSignature,
            r,
            rLength,
            id
            )
        return {'rhythmPatternID': rhythmPatternID,
                'rhythmDescription': rhythmDescription,
                'rhythmPattern': r,
                'rhythmLength': rLength,
                'timeSignature': timeSignature,
                'articulation': artic,
                }

    def getRandomRhythmPattern(self):
        patterns = self.getRhythmCollection().get('patterns')
        matchingRhythms = [pattern for pattern in patterns if pattern.get('rhythmLength') == self.notePatternDetails.get('noteLength')]
        if not matchingRhythms:
            return self.multipleBarRhythm()
        else:
            return random.choice(matchingRhythms)

    def getRhythmCollection(self):
        return next(collection for collection in self.collections if collection.get('collectionID') == self.rhythmCollectionID)

    def getNotePatternCollection(self):
        return next(collection for collection in self.collections if collection.get('collectionID') == self.primaryCollectionID)

    def selectExercise(self, collections, notePatternHistory):
        self.collections = collections
        self.notePatternHistory  = notePatternHistory
        if not self.reviewExercise or self.currentIndex < 1 and self.currentIndex < self.collectionLength:
            self.incrementMe = self.userProgramID
            self.incrementCurrentIndex()
            self.getNotePattern()
            self.determineDirection()
        else:
            self.getReviewNotePattern()
            self.applyNewDirection()
        if self.rhythmCollectionID:
            rhythmPatternDetails = self.getRandomRhythmPattern()
            self.rhythmPatternDetails = rhythmPatternDetails

    def storeExerciseAttributes(self, exerciseDetails):
        self.filename = exerciseDetails.get('imageFilename')
        self.exerciseID = exerciseDetails.get('exerciseID')
        self.description = exerciseDetails.get('description')
        self.exerciseName = exerciseDetails.get('exerciseName')

    def getDirectionPrep(direction):
        if direction == "ascending" or direction == "ascending descending":
            return 'to'
        elif direction == "descending" or direction == "descending ascending":
            return 'from'