import random
from objects.program import Program


class Player:
    def __init__(
        self,
        previousSet=None,
        program=None,
        exerciseHistory=None,
    ):
        if program is None:
            collections = [
                {
                    "title": "tone",
                    "currentKey": "g",
                    "currentMode": "major",
                    "index": 1,
                },
                {
                    "title": "ninthScale1",
                    "currentKey": "g",
                    "currentMode": "major",
                    "index": 1,
                },
            ]
            exerciseDetails = [
                {"key": "g", "mode": "major", "reviewBool": True, "type": "tone"},
                {"key": "g", "mode": "major", "reviewBool": False, "type": "tone"},
                {
                    "key": "g",
                    "mode": "major",
                    "reviewBool": True,
                    "type": "ninthScale1",
                },
                {
                    "key": "g",
                    "mode": "major",
                    "reviewBool": False,
                    "type": "ninthScale1",
                },
            ]
            self.__program = Program(collections, exerciseDetails, 3)
        else:
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
        for c in self.__program.getCollections:
            if c["title"] == collection:
                c["index"] = index
                break

    def incrementIndex(self, collection):
        for c in self.__program.getCollections:
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

    # @property
    # def getExerciseDetails(self):
    #     return self.__program["setPattern"]

    def setSetPattern(self, setPattern):
        self.__currenStatus["setPattern"] = setPattern

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
