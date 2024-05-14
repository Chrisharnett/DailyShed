"""
This class should take sessionData and the appropriate collections needed to build a session.
It will process those inputs and create the specific exercises for a new practice session.
"""
from practiceInterval import PracticeInterval
from setDesigner.queries import startUserPracticeSession, incrementProgramIndex, getNotePatternHistory, insertNewRhythmPattern
import random
import math


class PracticeSession:
    def __init__(self, sessionData, collections):
        self.__sessionData = sessionData
        self.__collections = collections
        self.__userPracticeSession = []
        self.__collectionHistory = []
        self.__exerciseDetails = []
        self.__userPracticeSessionID = None

    @property
    def userPracticeSession(self):
        return self.__userPracticeSession

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

    def minPlayCount(self, patterns):
        return min(pattern['playcount'] for pattern in patterns)

    def getReviewNotePattern(self, interval):
        notePatternHistory = getNotePatternHistory(self.__sessionData.get('sub'), interval.get('primaryCollectionID'))
        min = self.minPlayCount(notePatternHistory)
        reviewPatterns = [pattern for pattern in notePatternHistory if pattern.get('playcount') == min]
        notePatternID  = random.choice(reviewPatterns).get('notePatternID')
        directionIndex = next(pattern.get('directionIndex') for pattern in notePatternHistory if pattern.get('notePatternID') == notePatternID)
        coll = next(collection for collection in self.__collections if collection.get('collectionID') == interval.get('primaryCollectionID'))
        notePattern = next(pattern for pattern in coll.get('patterns') if pattern.get('notePatternID') == notePatternID)
        notePattern['currentDirectionIndex'] = (directionIndex + 1) % len(notePattern.get('directions'))
        return notePattern

    def incrementCurrentIndex(self, currentInterval):
        newIndex = currentInterval.get('currentIndex') + 1
        for interval in self.__sessionData.get('intervals'):
            if interval.get('userProgramID') == currentInterval.get('userProgramID'):
                interval['currentIndex'] = newIndex

    def getNotePattern(self, index, collectionID):
        for collection in self.__collections:
            if collection.get('collectionID') == collectionID:
                return collection.get('patterns')[index % len(collection.get('patterns'))]
        return None

    def maxRhythmNoteLength(self, rhythms):
        return max(rhythms.get('patterns'), key=lambda x: x.get('rhythmLength')).get('rhythmLength')

    def multipleBarRhythm(self, notePattern, rhythms):
        length = notePattern.get('noteLength')
        # maxRhythmLength = self.maxRhythmNoteLength(rhythms)
        # minimumNumberOfMeasures = math.ceil(length / maxRhythmLength)
        remainder = length
        r = []
        id = []
        rLength = 0
        artic = []
        while remainder > rhythms.get('patterns')[0].get('timeSignature')[0]:
            # Get the rhythms that are at least length/minNumberOfMeasures
            possibleRhythms = [
                x for x in rhythms.get('patterns') if remainder/2 <= x.get('rhythmLength') <= remainder
            ]
            measure = random.choice(possibleRhythms)
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
        random.shuffle(r)
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

    def getRandomRhythmPattern(self, notePattern, rhythmCollectionID):
        for collection in self.__collections:
            if collection.get('collectionID') == rhythmCollectionID:
                patterns = collection.get('patterns')
                matchingRhythms = [pattern for pattern in patterns if pattern.get('rhythmLength') == notePattern.get('noteLength')]
                if not matchingRhythms:
                    return self.multipleBarRhythm(notePattern, collection)
                else:
                    return random.choice(matchingRhythms)
        return None

    def createSession(self):
        self.setUserPracticeSessionID()
        for i, interval in enumerate(self.__sessionData.get('intervals')):
            print(f"{i}.{interval.get('PrimaryCollectionTitle')} - {interval.get('rhythmCollectionTitle')} - {interval.get('currentIndex')}")
            newInterval = PracticeInterval(interval)
            primaryCollectionID = interval.get('primaryCollectionID')
            rhythmCollectionID = interval.get('rhythmCollectionID')
            if not interval['reviewExercise'] or interval['currentIndex'] < 1 and interval['currentIndex'] < interval.get('collectionLength'):
                newInterval.incrementMe = interval.get('userProgramID')
                self.incrementCurrentIndex(interval)
                notePatternDetails = self.getNotePattern(newInterval.currentIndex, primaryCollectionID)
                newInterval.notePatternDetails = notePatternDetails
                newInterval.determineDirection()
            else:
                newInterval.notePatternDetails = self.getReviewNotePattern(interval)
                newInterval.applyNewDirection()
            if rhythmCollectionID:
                rhythmPatternDetails = self.getRandomRhythmPattern(newInterval.notePatternDetails, rhythmCollectionID)
                newInterval.rhythmPatternDetails = rhythmPatternDetails
            newInterval.createExercise(self.userPracticeSessionID)
            newExercise = {'exerciseID': newInterval.exerciseID,
                           'exerciseName': newInterval.exerciseName,
                           'filename': 'https://mysaxpracticeexercisebucket.s3.amazonaws.com/' + newInterval.filename,
                           'description': newInterval.description,
                           'incrementMe': newInterval.incrementMe
                           }
            print(f"{newInterval.notePatternID} - {newInterval.rhythmPatternID} - {newInterval.currentIndex} ")
            self.__userPracticeSession.append(newExercise)

