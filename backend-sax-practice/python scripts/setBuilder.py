from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns
from objects.practiceSet import PracticeSet
from objects.player import Player
import random


# build a set of setLength exercises from the setPattern.
def main():
    minNote = 1
    maxNote = 9
    maxLength = 2 * (maxNote)
    currentSetPattern = [{"type": 'tone', "reviewBool": 1, "key": 'g', 'mode': 'major'},
                      {"type": 'tone', "reviewBool": 0, "key": 'g', 'mode': 'major'},
                      {"type": 'ninthScale1', "reviewBool": 1, "key": 'g', 'mode': 'major'},
                      {"type": 'ninthScale1', "reviewBool": 0, "key": 'g', 'mode': 'major'}]

    player = Player(currentSetPattern)
    notes = notePatterns(minNote, maxNote, maxLength)
    rhythms = rhythmPatterns(4, 4)
    keys = ['g', 'c', 'd']
    practiceSet = PracticeSet(player, notes, rhythms)
    sessions = 20
    for i in range(sessions):

        currentSet = practiceSet.getNextSet()
        player.setPreviousSet(currentSet)
        print(f"day {i}")
        for exercise in currentSet:
            player.addExercise(exercise, random.randint(0, 5))
            print(exercise)
        print()
        player.setPreviousSet(currentSet)

if __name__ == '__main__':
    main()