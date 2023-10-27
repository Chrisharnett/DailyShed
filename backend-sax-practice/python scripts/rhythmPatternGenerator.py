from exerciseObjects import RhythmPattern, Collection
def noDuplicateRhythms(newPattern, patternList):
    for pattern in patternList:
        if pattern.getRhythmPattern == newPattern:
            return False
    # If the loop completes without finding a duplicate, add the new pattern
    return True

# TODO: Use rhythmPattern objects.
def rhythmPatterns(numerator, denominator):
    rhythm = str(denominator)
    rhythmPatternCollection = []
    rhythmId = 0
    toneRhythms = Collection('tone')
    toneRhythms.addPattern(RhythmPattern('tone' + "_" + str(rhythmId),
                                'tone',
                                [["1"]],
                                (numerator, denominator),
                                [{"articulation": "fermata",
                                  "index": 0,
                                  "name": "fermata"}]))
    rhythmId += 1

    toneRhythms.addPattern(RhythmPattern('tone' + "_" + str(rhythmId),
                                        'tone',
                                        [["1"], ["~"], ["1"]],
                                        (numerator, denominator),
                                         [{"articulation": "fermata",
                                         "index": 0,
                                         "name": "fermata"
                                          },{
                                          "articulation": "fermata",
                                          "index": 1,
                                          "name": ""}
                                          ]))

    rhythmId += 1

    rhythmPatternCollection.append(toneRhythms)

    quarterNoteOneBarRhythms = Collection("quarter note one bar rhythms")

    quarterNoteOneBarRhythms.addPattern(RhythmPattern('rhythm_' + str(rhythmId),
                                                      'one bar quarter note',
                                                      [["4"], ["4"], ["4"], ["4"]],
                                                      (numerator, denominator)))
    rhythmId += 1

    oneBarQuarterRests = [["r4"],["r4"],["r4"],["r4"]]

    # One pitch, 3 rests
    newPatterns=[]
    for i in range(numerator):
        oneBarQuarterNoteRhythm = [["r4"],["r4"],["r4"],["r4"]]
        oneBarQuarterNoteRhythm[i] = [rhythm]
        # newPattern = RhythmPattern("rhythm_" + str(rhythmId),
        #                            'one bar quarter note',
        #                            oneBarQuarterNoteRhythm,
        #                            (numerator, denominator))
        if noDuplicateRhythms(oneBarQuarterNoteRhythm, quarterNoteOneBarRhythms):
            quarterNoteOneBarRhythms.addPattern(RhythmPattern("rhythm_" + str(rhythmId),
                                                              'one bar quarter note',
                                                              oneBarQuarterNoteRhythm,
                                                              (numerator, denominator)))
            rhythmId += 1



    for i in range(numerator):
        newPatterns = []
        for j in range(1 + i, numerator):
            oneBarQuarterNoteRhythm = oneBarQuarterRests.copy()
            oneBarQuarterNoteRhythm[i] = ["4"]
            oneBarQuarterNoteRhythm[j] = ["4"]
            # newPattern = {"rhythmPattern": oneBarQuarterNoteRhythm,
            #               "timeSignature": (numerator, denominator),
            #               "rhythm": "quarter note",
            #               "articulation": [],
            #               "dynamic": ""}
            if noDuplicateRhythms(oneBarQuarterNoteRhythm, quarterNoteOneBarRhythms):
                quarterNoteOneBarRhythms.addPattern(RhythmPattern("rhythm_" + str(rhythmId),
                                                                  'one bar quarter note',
                                                                  oneBarQuarterNoteRhythm,
                                                                  (numerator, denominator)))
                rhythmId += 1

    quarterNoteOneBarRhythms.addPattern(RhythmPattern("rhythm_" + str(rhythmId),
                                        'one bar quarter note',
                                        [["r4"], ["r4"], ["4"], ["4"]],
                                        (numerator, denominator)))
    rhythmId += 1

    oppositePatterns = []
    for pattern in quarterNoteOneBarRhythms:
        newPattern = []
        for r in pattern:
            if r[0] == "4":
                newPattern.append(["r4"])
            elif r[0] == "r4":
                newPattern.append(["4"])
        oppositePatterns.append(newPattern)

    for newPattern in oppositePatterns:
        if (noDuplicateRhythms(newPattern, quarterNoteOneBarRhythms)):
            quarterNoteOneBarRhythms.addPattern(RhythmPattern("rhythm_" + str(rhythmId),
                                                              'one bar quarter note',
                                                              newPattern,
                                                              (numerator, denominator)))
            rhythmId += 1

    return quarterNoteOneBarRhythms

def main():
    # Time signature. Numerator has to be int, denominator a string.
    numerator = 4
    denominator = "4"
    rhythms = rhythmPatterns(numerator, denominator)
    for rhythmType in rhythms:
        for patterns in rhythmType.get('rhythmPatterns'):
            print(patterns.get('rhythmPattern'))



if __name__ == '__main__':
    main()