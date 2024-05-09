"""
This class should take sessionData and the appropriate collections needed to build a session pattern.
It will process those inputs and create the specific exercises for a new practice session.
"""
from practiceInterval import PracticeInterval
from setDesigner.queries import startUserPracticeSession
import random
import math


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

    def maxRhythmNoteLength(self, rhythms):
        return max(rhythms.get('patterns'), key=lambda x: x.get('rhythmLength')).get('rhythmLength')

    def multipleBarRhythm(self, notePattern, rhythms):
        length = notePattern.get('noteLength')
        maxRhythmLength = self.maxRhythmNoteLength(rhythms)
        minimumNumberOfMeasures = math.ceil(length / maxRhythmLength)
        # measureNumber = 0
        remainder = length
        r = []
        id = "Multi"
        rLength = 0
        artic = []
        while remainder > maxRhythmLength:
            # Get the rhythms that are at least length/minNumberOfMesures
            possibleRhythms = [
                x for x in rhythms.get('patterns') if length / minimumNumberOfMeasures <= x.get('rhythmLength')
            ]
            measure = random.choice(possibleRhythms)
            r.extend(measure.get('rhythmPattern'))
            id += str(measure.get('rhythmPatternId'))
            rLength += measure.get('rhythmLength')
            remainder -= measure.get('rhythmLength')
            if measure.get('articulation'):
                artic.extend(measure.get('articulation'))
        possibleRhythms = [x for x in rhythms.get('patterns') if x.get('rhythmLength') == remainder]
        lastMeasure = random.choice(possibleRhythms)
        rLength += lastMeasure.get('rhythmLength')
        if lastMeasure.get('articulation'):
            artic.extend(lastMeasure.get('articulation'))
        r.extend(lastMeasure.get('rhythmPattern'))
        random.shuffle(r)
        return {'rhythmPatternID': id,
                'rhythmDescription': lastMeasure.get('rhythmDescription'),
                'rhythmPattern': r,
                'rhythmLength': rLength,
                'timeSignature': lastMeasure.get('timeSignature'),
                'articulation': artic,
                }

    def getRandomRhythmPattern(self, notePattern, rhythmCollectionID):
        for collection in self.__collections:
            if collection.get('collectionID') == rhythmCollectionID:
                patterns = collection.get('patterns')
                matchingRhythms = [pattern for pattern in patterns if pattern.get('rhythmLength') == notePattern.get('noteLength')]
                choice = random.choice(matchingRhythms)
                if not choice:
                    choice = self.multipleBarRhythm(notePattern, collection)
                return choice
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
            print(newInterval.exerciseName)
            self.__practiceSession.append(newExercise)

