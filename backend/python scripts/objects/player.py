import random

class Player:
    def __init__(self, previousSet=None, currentStatus=None, exerciseHistory=None, ):
        if currentStatus is None:
            self.__currentStatus = {'setPattern': [{"type": 'tone', "reviewBool": 1, "key": 'g', 'mode': 'major'},
                                                   {"type": 'tone', "reviewBool": 0, "key": 'g', 'mode': 'major'},
                                                   {"type": 'ninthScale1', "reviewBool": 1, "key": 'g', 'mode': 'major'},
                                                   {"type": 'ninthScale1', "reviewBool": 0, "key": 'g', 'mode': 'major'}],
                             'currentIndex': {'tone': {'index': -1,
                                                       'currentKey': 'g',
                                                       'currentMode': 'major'},
                                              'ninthScale1': {'index': -1,
                                                              'currentKey': 'g',
                                                              'currentMode': 'major'}}
                            }
        else:
            self.__currentStatus = currentStatus
        if exerciseHistory is None:
            self.__exerciseHistory = []
        else:
            self.__exerciseHistory = exerciseHistory
        if previousSet is None:
            self.__previousSet = []
        self.__previousSet = previousSet

    @property
    def getCurrentStatus(self):
        return self.__currentStatus

    def getIndex(self, collection):
        index = self.__currentStatus['currentIndex'][collection]['index']
        if index:
            return index

    def setIndex(self, collection, index):
        self.__currentStatus['currentIndex'][collection]['index'] = index

    def incrementIndex(self, collection):
        self.__currentStatus['currentIndex'][collection]['index'] +=1

    @property
    def getPreviousSet(self):
        return self.__previousSet

    def setPreviousSet(self, set):
        pSet = []
        for exercise in set:
            pSet.append(exercise.serialize())
        self.__previousSet = pSet

    @property
    def getSetPattern(self):
        return self.__currentStatus['setPattern']

    def setSetPattern(self, setPattern):
        self.__currenStatus['setPattern'] = setPattern

    @property
    def exerciseHistory(self):
        if self.__exerciseHistory:
            return self.__exerciseHistory

    def getIndex(self, collection):
        index = self.__currentStatus['currentIndex'][collection]['index']
        if index:
            return index

    def addExercise(self, exercise, assessment):
        for ex in self.__exerciseHistory:
            if exercise == ex:
                ex['assessment'] = assessment
                ex['playCount'] = ex['playCount'] + 1
                return
        self.__exerciseHistory.append({'exercise': exercise.serialize(),
                                       'assessment': assessment,
                                       'playCount': 1})
