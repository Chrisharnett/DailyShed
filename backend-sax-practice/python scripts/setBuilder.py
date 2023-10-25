from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns
from exerciseObjects import Set

# build a set of setLength exercises from the setPattern.


def main():
    minNote = 1
    maxNote = 9
    maxLength = 2 * (maxNote)
    setLength = 4
    currentSetPattern = [{"type": 'tone', "reviewBool": 1},
                      {"type": 'tone', "reviewBool": 0},
                      {"type": 'scale1', "reviewBool": 1},
                      {"type": 'scale1', "reviewBool": 0}]
    previousSet = []
    newSet = Set(setLength, currentSetPattern, notePatterns(minNote, maxNote, maxLength), rhythmPatterns(4, 4), previousSet)




if __name__ == '__main__':
    main()