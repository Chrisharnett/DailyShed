"""
This class should take sessionData and the appropriate collections needed to build a session.
It will process those inputs and create the specific exercises for a new practice session.
"""
from queries.queries import startUserPracticeSession, getNotePatternHistory, addNewExercise, fetchExercise
from util.imageURL import imageURL
from objects.UserExercise import UserExercise


class PracticeSession:
    def __init__(self, sub, userName, rounds, setLength, userPracticeSession = None, collectionHistory = None, exerciseDetails = None, collections = None):
        # self.__sessionData = sessionData
        self.__sub = sub
        self.__userName = userName
        self.__rounds = rounds
        self.__setLength = setLength
        self.__collectionHistory = collectionHistory or []
        self.__exerciseDetails = exerciseDetails or []
        self.__intervals = []
        self.__userPracticeSessionID = startUserPracticeSession(self.sub)
        self.__userPracticeSession = userPracticeSession or []
        self.__collections = collections

    @property
    def sub(self):
        return self.__sub

    @sub.setter
    def sub(self, sub):
        self.__sub = sub

    @property
    def userName(self):
        return self.__userName

    @userName.setter
    def userName(self, userName):
        self.__userName = userName

    @property
    def rounds(self):
        return self.__rounds

    @rounds.setter
    def rounds(self, rounds):
        self._round = rounds

    @property
    def setLength(self):
        return self.__setLength

    @setLength.setter
    def setLength(self, setLength):
        self.__setLength = setLength

    @property
    def userPracticeSession(self):
        return self.__userPracticeSession

    @userPracticeSession.setter
    def userPracticeSession(self, userPracticeSession):
        self.__userPracticeSession = userPracticeSession

    def addExerciseToPracticeSession(self, exercise):
        self.__userPracticeSession.append(exercise)

    @property
    def collectionHistory(self):
        return self.__collectionHistory

    @collectionHistory.setter
    def collectionHistory(self, history):
        self.__collectionHistory = history

    @property
    def exerciseDetails(self):
        return self.__exerciseDetails

    @exerciseDetails.setter
    def exerciseDetails(self, details):
        self.__exerciseDetails = details

    @property
    def intervals(self):
        return self.__intervals

    @intervals.setter
    def intervals(self, intervals):
        self.__intervals = intervals

    def addInterval(self, interval):
        self.__intervals.append(interval)

    @property
    def userPracticeSessionID(self):
        return self.__userPracticeSessionID

    @userPracticeSessionID.setter
    def userPracticeSessionID(self, value):
        self.__userPracticeSessionID = value

    @property
    def collections(self):
        return self.__collections

    @collections.setter
    def collections(self, collections):
        self.__collections = collections

    def addCollection(self, collection):
        self.__collections.append(collection)

    def addExerciseToSession(self, exercise):
        self.__exerciseDetails.append(exercise)

    def getNewExercise(self, interval):
        pass

    def insertExercise(self, userPracticeSessionID, interval):
        direction = None
        if interval.directionIndex:
            direction = interval.directions[interval.directionIndex]
        interval.setDetails()
        insertedExercise = addNewExercise([
            interval.notePatternID,
            interval.rhythmPatternID,
            interval.tonic,
            interval.mode,
            direction,
            interval.directionIndex,
            interval.userProgramID,
            userPracticeSessionID,
            interval.exerciseName,
            interval.description])
        interval.storeExerciseAttributes(insertedExercise)
        return insertedExercise

    def createSession(self):
        intervalID = 0
        for interval in self.intervals:
            notePatternHistory = getNotePatternHistory(self.sub, interval.primaryCollectionID)
            interval.selectExercise(self.collections, notePatternHistory)
            # Increment for following exercises in this set.
            if interval.incrementMe:
                for i in self.intervals:
                    if interval.userProgramID == i.userProgramID:
                        i.currentIndex = interval.currentIndex
            exerciseDetails = fetchExercise(
                interval.notePatternID,
                interval.rhythmPatternID,
                interval.tonic,
                interval.mode,
                interval.directionIndex)
            if not exerciseDetails:
                interval.exerciseID = self.insertExercise(self.userPracticeSessionID, interval).get('exerciseID')
            else:
                # FIXME
                interval.storeExerciseAttributes(exerciseDetails)
            # interval.createTestImage(intervalID)
            intervalID += 1
            interval.createImage()
            intervalExercise = UserExercise(interval.exerciseID, interval.exerciseName, imageURL(interval.filename), interval.description, interval.incrementMe)
            self.addExerciseToPracticeSession(intervalExercise)

