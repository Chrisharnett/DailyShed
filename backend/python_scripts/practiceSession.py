"""
This class should take sessionData and the appropriate collections needed to build a session pattern.
It will process those inputs and create the specific exercises for a new practice session.
"""
from practiceInterval import PracticeInterval
import random

class PracticeSession:
    def __init__(self, sessionData, collections):
        self.__sessionData = sessionData
        self.__collections = collections
        self.__practiceSession = []
        self.__collectionHistory = []
        self.__exerciseDetails = []

    @property
    def getPracticeSession(self):
        return self.__exerciseDetails

    def addExerciseToSession(self, exercise):
        self.__exerciseDetails.appent(exercise)

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
        for i, interval in enumerate(self.__sessionData):
            newInterval = PracticeInterval(interval)
            primaryCollectionID = interval['primaryCollectionID']
            rhythmCollectionID = interval['rhythmCollectionID']
            if not interval['reviewExercise'] or interval['currentIndex'] < 1:
                index = self.incrementCurrentIndex(primaryCollectionID)
                notePattern = self.getNotePattern(index, primaryCollectionID)
                newInterval.setNotePatternID(notePattern)
                newInterval.setDirection()
                if rhythmCollectionID:
                    rhythmPatternID = self.getRandomRhythmPattern(notePattern, rhythmCollectionID)
                    newInterval.setRhythmPatternDetails(rhythmPatternID)
                    newInterval.createExercise()
            else:
                exercise = self.getReviewExercise(self, primaryCollectionID)

            self.__practiceSession.append(newInterval)
            """
            Check if exercise exists. If so, return it. If not, create a new exerciseImage and insert the exercise in the DB
            """


                # self.__practiceSession.append(newExercise)

            # else:
                # newExercise, updatedProgram = createNewNoteExercise(exercise, history, previousSet, program)
                # newExercise = getNewExercise(interval)
                #
                # if newExercise is None:
                #     newExercise = createReviewNoteExercise(interval, history)
                # newSet.append(newExercise)
                # # player['program'] = updatedProgram
        # return newSet, player



# TODO: Choose direction and adjust noteLength before getting selecting rhythmPattern

