class UserExercise:
    def __init__(self, exerciseID, exerciseName, filename, description, incrementMe):
        self.__exerciseID = exerciseID
        self.__exerciseName = exerciseName
        self.__filename = filename
        self.__description = description
        self.__incrementMe = incrementMe

    @property
    def exerciseID(self):
        return self.__exerciseID

    @exerciseID.setter
    def exerciseID(self, exerciseID):
        self.__exerciseID = exerciseID

    @property
    def exerciseName(self):
        return self.__exerciseName

    @exerciseName.setter
    def exerciseName(self, exerciseName):
        self.__exerciseName = exerciseName

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        self.__filename = filename

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def incrementMe(self):
        return self.__incrementMe

    @incrementMe.setter
    def incrementMe(self, incrementMe):
        self.__incrementMe = incrementMe

    def toDict(self):
        return {
            "exerciseID": self.__exerciseID,
            "exerciseName": self.__exerciseName,
            "filename": self.__filename,
            "description": self.__description,
            "incrementMe": self.__incrementMe
        }