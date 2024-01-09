from objects.player import Player
from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns
from objects.practiceSet import PracticeSet
import boto3
import json
import datetime

s3_client = boto3.client("s3")

def getPlayer():
    with open('testJSON/playerJSON.json', 'r') as file:
        data = json.load(file)
    player = Player(data.previousSet, data.currentStatus, data.exerciseHistory)
    return player

def main():
    bucketName = "mysaxpracticeexercisebucket"
    player = Player()
    minNote = 1
    maxNote = 9
    notes = notePatterns(minNote, maxNote, (2 * maxNote))
    rhythms = rhythmPatterns(4, 4)
    sets = 2

    currentRound = 1
    while currentRound <= sets:
        practiceSet = PracticeSet(player, notes, rhythms)
        currentSet = practiceSet.getNextSet()
        returnSet = []

        i = 0
        while i < 3:
            for exercise in currentSet:
                try:
                    objectKey = exercise.exerciseFileName()
                    s3_client.head_object(Bucket=bucketName, Key=objectKey)
                except Exception as e:
                    exercise.createImage()
                e = exercise.serialize()
                url = exercise.imageURL()
                returnSet.append(exercise)
                player.addExercise(exercise, datetime.datetime.now(), 3)
                print(exercise)
            player.setPreviousSet(currentSet)
            i += 1

        currentRound += 1

    print('complete')

if __name__ == '__main__':
    main()