import random

class Player:
    def __init__(self, pattern, collectionIndices=None):
        if collectionIndices is None:
            collectionIndices = {'tone': {'currentIndex': -1,
                                          'currentKey': 'g',
                                          'currentMode': 'major'},
                                 'ninthScale1': {'currentIndex': -1,
                                                 'currentKey': 'g',
                                                 'currentMode': 'major'}}
        self.__pattern = pattern
        self.__exerciseHistory = {}
        self.__collectionIndices = collectionIndices
        self.__previousSet = []
    @property
    def getCollectionIndices(self):
        return self.__collectionIndices

    def incrementIndex(self, collection):
        self.__collectionIndices[collection]['currentIndex'] +=1

    @property
    def getPreviousSet(self):
        return self.__previousSet

    def setPreviousSet(self, set):
        self.__previousSet = set

    @property
    def getCurrentCollection(self):
        return self.__currentCollection

    def setCurrentCollection(self, collection):
        self.__currentCollection = collection

    @property
    def getSetPattern(self):
        return self.__pattern

    def setSetPattern(self, setPattern):
        self.__setPattern = setPattern

    @property
    def exerciseHistory(self):
        if self.__exerciseHistory:
            return self.__exerciseHistory

    def addExercise(self, exercise, assessment):
        for ex in self.__exerciseHistory:
            if exercise == ex:
                ex['assessment'] = assessment
                ex['playCount'] = ex['playCount'] + 1
                return
        self.__exerciseHistory[exercise.exerciseFileName] = {'exercise': exercise,
                                                'assessment': assessment,
                                                'playCount': 1}