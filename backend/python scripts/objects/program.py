class Program:
    def __init__(
        self,
        collections,
        exerciseDetails,
        rounds=3,
    ):
        self.__collections = collections
        self.__exerciseDetails = exerciseDetails
        self.__rounds = rounds

    @property
    def getCollections(self):
        return self.__collections

    @property
    def getExerciseDetails(self):
        return self.__exerciseDetails

    @property
    def getRounds(self):
        return self.__rounds
