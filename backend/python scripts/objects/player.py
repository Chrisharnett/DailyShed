import random
from objects.program import Program


class Player:
    def __init__(
        self,
        previousSet=None,
        program=None,
        exerciseHistory=None,
    ):
        self.__program = program
        if exerciseHistory is None:
            self.__exerciseHistory = []
        else:
            self.__exerciseHistory = exerciseHistory
        if previousSet is None:
            self.__previousSet = []
        self.__previousSet = previousSet

    @property
    def getProgram(self):
        return self.__program

    def getIndex(self, collection):
        for c in self.__program["collections"]:
            if c["title"] == collection:
                return c["index"]
        return None

    def setIndex(self, collection, index):
        for c in self.getProgram["collections"]:
            if c["title"] == collection:
                c["index"] = index
                break

    def incrementIndex(self, collection):
        for c in self.getProgram["collections"]:
            if c["title"] == collection:
                c["index"] += 1
                break

    @property
    def getPreviousSet(self):
        return self.__previousSet

    def setPreviousSet(self, set):
        pSet = []
        for exercise in set:
            pSet.append(exercise.serialize())
        self.__previousSet = pSet

    # def setSetPattern(self, setPattern):
    #     self.__currenStatus["setPattern"] = setPattern

    @property
    def exerciseHistory(self):
        if self.__exerciseHistory:
            return self.__exerciseHistory

    def getIndex(self, collection):
        index = self.__program["currentIndex"][collection]["index"]
        if index:
            return index

    def addExercise(self, exercise, timeStamp, assessment):
        self.__exerciseHistory.append(
            {
                "exercise": exercise.serialize(),
                "assessment": assessment,
                "timeStamp": timeStamp,
            }
        )
