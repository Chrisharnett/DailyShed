import random
from setDesigner.notePatterns import getNotePatternRhythmLength
from setDesigner.queries import fetchExercise, addNewExercise
from setDesigner.exerciseObjects import Exercise

class PracticeInterval:
    def __init__(self, interval):
        self.__interval = interval
        self.__notePatternDetails = {}
        self.__rhythmPatternDetails = {}
        self.__exerciseID = None
        self.__directionIndex = None

    @property
    def getNotePatternID(self):
        return self.__notePatternDetails.get('notePatternID')

    @property
    def getRhythmPatternID(self):
        return self.__rhythmPatternDetails.get('notePatternID')

    def setNotePatternID(self, notePatternID):
        self.__notePatternDetails = notePatternID

    @property
    def getDirections(self):
        return self.__notePatternDetails['directions']

    @property
    def getDirectionIndex(self):
        return self.__directionIndex

    def getCurrentDirection(self):
        if self.getDirectionIndex:
            return self.getDirections[self.getDirectionIndex]
        return None

    def setNoteLength(self, length):
        self.__notePatternDetails['noteLength'] = length

    def setDirection(self):
        currentDirectionIndex = self.__notePatternDetails.get('directionIndex')
        directions = self.__notePatternDetails.get('directions')
        if not currentDirectionIndex:
            self.__directionIndex =  '0'
        elif currentDirectionIndex < len(directions):
            newIndex = currentDirectionIndex + 1
            self.__directionIndex = newIndex
        elif currentDirectionIndex == 'r' or currentDirectionIndex == (len(directions) -1):
            validDirectionIndices =[i for i in range(len(directions)) if i != self.__notePatternDetails.get('currentDirectionIndex')]
            self.__directionIndex = random.choice(validDirectionIndices)
        self.applyNewDirection()

    def applyNewDirection(self):
        direction = self.getDirections[int(self.__directionIndex)]
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
        d = self.__notePatternDetails.get('notePattern').copy()
        d.reverse()
        self.__notePatternDetails['notePattern'] = d
        self.newNoteLength()

    def ascendingDescendingPattern(self):
        a = self.__notePatternDetails.get('notePattern').copy()
        d = self.__notePatternDetails.get('notePattern').copy()
        d.reverse()
        a.pop()
        a.extend(d)
        self.__notePatternDetails['notePattern'] = a
        self.newNoteLength()

    def descendingAscendingPattern(self):
        d = self.__notePatternDetails.get('notePattern').copy()
        d.reverse()
        d.pop()
        d.extend(self.__notePatternDetails.get('notePattern'))
        self.__notePatternDetails['notePattern'] = d
        self.newNoteLength()

    def newNoteLength(self):
        newLength = getNotePatternRhythmLength(self.__notePatternDetails.get('notePattern'), self.__notePatternDetails.get('holdLastNote'))
        self.setNoteLength(newLength)

    @property
    def getTonic(self):
        return self.__interval.get('tonic')

    @property
    def getMode(self):
        return self.__interval.get('mode')

    @property
    def getTimeSignature(self):
        return self.__rhythmPatternDetails.get('timeSignature')

    @property
    def getRhythmDescription(self):
        return self.__rhythmPatternDetails.get('rhythmDescription')

    @property
    def getRhythmPatternDetails(self):
        return self.__rhythmPatternDetails

    @property
    def getRhythmPattern(self):
        return self.__rhythmPatternDetails.get('rhythmPattern')

    @property
    def getCollectionTitle(self):
        return self.__interval.get('primaryCollectionTitle')

    @property
    def getNotePattern(self):
        return self.__notePatternDetails.get('notePattern')

    @property
    def getProgramID(self):
        return self.__interval('programID')

    def setRhythmPatternDetails(self, rhythmPatternDetails):
        self.__rhythmPatternDetails = rhythmPatternDetails

    def getExerciseDetails(self):
        pass

    def createExercise(self):
        """
        These attributes are able to ID an exercise. It may need to change over time.
         notePatternID, rhythmPatternID, tonic, mode, directionIndex
        """
        exerciseDetails = fetchExercise(
            self.getNotePatternID,
            self.getRhythmPatternID,
            self.getTonic,
            self.getMode,
            self.getDirectionIndex)
        if not exerciseDetails:
            self.exerciseImageMaker()
        else:
            self.__exerciseDetails = exerciseDetails

    def insertExercise(self):
        addNewExercise(
            self.getNotePatternID,
            self.getRhythmPatternID,
            self.getTonic,
            self.getMode,
            self.getCurrentDirection,
            self.getDirectionIndex,
            self.getProgramID,)

    def exerciseImageMaker(self):
        pitches = self.getNotePattern
        rhythm = self.getRhythmPattern
        key = self.getTonic
        mode = self.getMode
        preamble = 'preamble', r"#(set-global-staff-size 28)"
        exercise = Exercise(pitches, rhythm, key, mode, preamble)
        self.insertExercise()
        exercise.createImage()



    def getDirectionPrep(direction):
        if direction == "ascending" or direction == "ascending descending":
            return 'to'
        elif direction == "descending" or direction == "descending ascending":
            return 'from'