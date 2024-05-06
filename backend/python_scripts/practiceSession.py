"""
This class should take sessionData and the appropriate collections needed to build a session pattern.
It will process those inputs and create the specific exercises for a new practice session.
"""
from practiceInterval import PracticeInterval
from setDesigner.queries import startUserPracticeSession
import random


class PracticeSession:
    def __init__(self, sessionData, collections):
        self.__sessionData = sessionData
        self.__collections = collections
        self.__practiceSession = []
        self.__collectionHistory = []
        self.__exerciseDetails = []
        self.__userPracticeSessionID = None

    @property
    def practiceSession(self):
        return self.__practiceSession

    @property
    def userPracticeSessionID(self):
        return self.__userPracticeSessionID

    @property
    def rounds(self):
        return self.__sessionData.get('rounds')

    def setUserPracticeSessionID(self):
        if not self.userPracticeSessionID:
            self.__userPracticeSessionID = startUserPracticeSession(self.__sessionData.get('sub'))

    def addExerciseToSession(self, exercise):
        self.__exerciseDetails.append(exercise)

    def setCollectionHistory(self, history):
        self.__collectionHistory = history

    def getNewExercise(self, interval):
        pass

    def getReviewExercise(self, interval):
        pass

    def incrementCurrentIndex(self, collectionID):
        for collection in self.__collections:
            if collection.get('collectionID') == collectionID:
                newIndex = collection.get('currentIndex') + 1
                collection['currentIndex']  = newIndex
                return newIndex
        return None

    def getNotePattern(self, index, collectionID):
        for collection in self.__collections:
            if collection.get('collectionID') == collectionID:
                return collection.get('patterns')[index]
        return None

    def getRandomRhythmPattern(self, notePattern, rhythmCollectionID):
        for collection in self.__collections:
            if collection.get('collectionID') == rhythmCollectionID:
                patterns = collection.get('patterns')
                matchingRhythms = [pattern for pattern in patterns if pattern.get('rhythmLength') == notePattern.get('noteLength')]
                return random.choice(matchingRhythms)
        return None

    def createSession(self):
        self.setUserPracticeSessionID()
        for i, interval in enumerate(self.__sessionData.get('intervals')):
            newInterval = PracticeInterval(interval)
            primaryCollectionID = interval.get('primaryCollectionID')
            rhythmCollectionID = interval.get('rhythmCollectionID')
            if not interval['reviewExercise'] or interval['currentIndex'] < 1:
                index = self.incrementCurrentIndex(primaryCollectionID)
                notePatternDetails = self.getNotePattern(index, primaryCollectionID)
                newInterval.notePatternDetails = notePatternDetails
                newInterval.determineDirection()
                if rhythmCollectionID:
                    rhythmPatternDetails = self.getRandomRhythmPattern(notePatternDetails, rhythmCollectionID)
                    newInterval.rhythmPatternDetails = rhythmPatternDetails

            else:
                exercise = self.getReviewExercise(self, self.primaryCollectionID)

            newInterval.createExercise(self.userPracticeSessionID)
            newExercise = {'exerciseID': newInterval.exerciseID,
                           'exerciseName': newInterval.exerciseName,
                           'filename': 'https://mysaxpracticeexercisebucket.s3.amazonaws.com/' + newInterval.filename,
                           'description': newInterval.description}
            self.__practiceSession.append(newExercise)

