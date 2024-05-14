import random
from setDesigner.notePatterns import getNotePatternRhythmLength
from setDesigner.queries import fetchExercise, addNewExercise
from exercise import Exercise

class PracticeInterval(Exercise):
    def __init__(self, interval):
        super().__init__(tonic = interval.get('tonic'), mode = interval.get('mode'))
        self.__interval = interval
        self.__notePatternDetails = {}
        self.__rhythmPatternDetails = {}
        self.__incrementMe = False

    @property
    def currentIndex(self):
        return self.__interval.get('currentIndex')

    @currentIndex.setter
    def currentIndex(self, index):
        self.__interval['currentIndex'] = index

    @property
    def incrementMe(self):
        return self.__incrementMe

    @incrementMe.setter
    def incrementMe(self, userProgramID):
        self.__incrementMe = userProgramID

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
    def noteLength(self):
        return self.__notePatternDetails.get('noteLength')

    @noteLength.setter
    def noteLength(self, length):
        self.__notePatternDetails['noteLength'] = length

    @property
    def getRhythmDescription(self):
        return self.__rhythmPatternDetails.get('rhythmDescription')

    @property
    def getCollectionTitle(self):
        return self.__interval.get('primaryCollectionTitle')

    @property
    def userProgramID(self):
        return self.__interval.get('userProgramID')

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
        newLength = getNotePatternRhythmLength(self.notePattern, self.holdLastNote)
        self.noteLength = newLength

    def createExercise(self, userPracticeSessionID):
        """
        These attributes are able to ID an exercise. It may need to change over time.
         notePatternID, rhythmPatternID, tonic, mode, directionIndex
        """

        exerciseDetails = fetchExercise(
            self.notePatternID,
            self.rhythmPatternID,
            self.tonic,
            self.mode,
            self.directionIndex)
        if not exerciseDetails:
            # FIXME
            exerciseID = self.insertExercise(userPracticeSessionID)
            # self.filename = exerciseID
            self.createImage()
        else:
            # FIXME
            self.storeExerciseAttributes(exerciseDetails)
            # self.createImage()
            # insert exercise into practice session.

    def storeExerciseAttributes(self, exerciseDetails):
        self.filename = exerciseDetails.get('imageFilename')
        self.exerciseID = exerciseDetails.get('exerciseID')
        self.description = exerciseDetails.get('description')
        self.exerciseName = exerciseDetails.get('exerciseName')

    def insertExercise(self, userPracticeSessionID):
        insertedExercise = addNewExercise(
            self.notePatternID,
            self.rhythmPatternID,
            self.tonic,
            self.mode,
            self.directions[self.directionIndex],
            self.directionIndex,
            self.userProgramID,
            userPracticeSessionID)
        self.storeExerciseAttributes(insertedExercise)

    def getDirectionPrep(direction):
        if direction == "ascending" or direction == "ascending descending":
            return 'to'
        elif direction == "descending" or direction == "descending ascending":
            return 'from'