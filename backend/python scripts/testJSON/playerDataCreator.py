from objects.player import Player
from objects.practiceSet import PracticeSet
from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns
import json
import random
import csv


def writeJSON(data):
    fields = ["name", "history", "currentStatus", "previousSet"]

    jsonExercises = json.dumps(data)
    with open("playerJSON.json", 'w') as file:
        file.write(jsonExercises)

def createPlayerData():
    # players = ['Chris', 'Paula', 'Samuel', 'Miguel', 'Susan', 'Isla', 'Lexi']
    players = ['Chris']
    minNote = 1
    maxNote = 9
    notes = notePatterns(minNote, maxNote, (2 * maxNote))
    rhythms = rhythmPatterns(4, 4)

    data=[]
    for player in players:
        p = Player()
        for i in range(random.randint(1, 2)):
            s = PracticeSet(p, notes, rhythms)
            currentSet = s.getNextSet()
            for exercise in currentSet:
                p.addExercise(exercise, random.randint(0, 5))
            p.setPreviousSet(currentSet)
        data.append({"name": player,
                     "exerciseHistory": p.exerciseHistory,
                     "currentStatus": p.getProgram,
                     "previousSet": p.getPreviousSet})

    writeJSON(data)


def main():
    data = createPlayerData()
if __name__ == '__main__':
    main()