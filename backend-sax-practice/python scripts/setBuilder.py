from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns
from exerciseObjects import PracticeSet

# build a set of setLength exercises from the setPattern.


def main():
    minNote = 1
    maxNote = 9
    maxLength = 2 * (maxNote)
    currentSetPattern = [{"type": 'tone', "reviewBool": 1},
                      {"type": 'tone', "reviewBool": 0},
                      {"type": 'scale1', "reviewBool": 1},
                      {"type": 'scale1', "reviewBool": 0}]
    previousSet = None
    player = None
    notes = notePatterns(minNote, maxNote, maxLength)
    rhythms = rhythmPatterns(4, 4)
    practiceSet = PracticeSet(currentSetPattern, notes, rhythms)
    practiceSet.getNextSet(previousSet, player)



if __name__ == '__main__':
    main()