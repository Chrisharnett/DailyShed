from notePatternGenerator import notePatterns
from rhythmPatternGenerator import rhythmPatterns

preamble = r"""#(set-global-staff-size 14)
        """
def makeFirstSet(routinePattern, notePatternDictionary, rhythmPatternDictionary):
    newSet = []
    for i in range(len(routinePattern)):
        if routinePattern[i] == 'longTone':
            rhythms = list(filter(lambda x: x.get('rhythmType') == routinePattern[i], rhythmPatternDictionary))
            for n in notePatternDictionary:
                for r in rhythms.get('rhythmPatterns'):
                    if ((len(r.rhythmPattern) == len(n)) or (len(n) == len(r.rhythmPattern) - sum(1 for x in n if x == ['~']))):
                        note = []
                        for i in range(len(n)):
                            note = [n[i], r[i]]
                            print(note)
            # newSet[i]
    return newSet
def creatingPatterns():
    # for the number of notes(!contain r) in a rhythmPattern, combine with a notepattern of the same length -1 (last note is held).
    # Use a filter.
    # if notes > max number of notes in rhythms, combine rhythms to the length of the notepattern.
    # create a pattern with the combined lists.
    #
    pass

def main():
    # TODO: Min note and max note for range. Attach to instruments
    minNote = 1
    maxNote = 9
    maxLength = 2 * (maxNote)
    routinePattern = ['longTone', 'longTone', 'scale', 'scale']
    notePatternDictionary = notePatterns(minNote, maxNote, maxLength)
    rhythmPatternDictionary = rhythmPatterns(4, 4)
    previousSet = []
    # newSet = []
    if len(previousSet) == 0:
        newSet = makeFirstSet(routinePattern, notePatternDictionary, rhythmPatternDictionary)
        print(newSet)


    # createSession(routinePattern, notePatternDictionary, rhythmPatternDictionary)
    # exercisePatterns = []
    # for r in rhythmPatternDictionary:
    #     for p in r.get('rhythmPatterns'):
    #         for n in notePatternDictionary:
    #             if len(p.rhythmPattern) == len(n) or (len(n) == len(p.rhythmPattern) - sum(1 for x in n if x == ['~'])):
    #                 newExPattern = []



if __name__ == '__main__':
    main()


pattern = {
"patternType": "scale",
"notePattern": [["repeat", [1, "4"], [2, "4"], [3, "4"], [4, "4"],
                 [5, "4"], [4, "4"], [3, "4"], [2, "4"]],
                [1, "1"]],
"preamble": preamble,
"description": "Play each note evenly. Repeat as many times as you can!",
"timeSignature": (4, 4),
"rhythm": "quarter_note",
"articulation": [],
"dynamic": "",
"direction": "ascending, descending"
}