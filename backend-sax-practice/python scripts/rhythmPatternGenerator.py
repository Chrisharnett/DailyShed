
def noDuplicateRhythms(newPattern, patternList):
    for pattern in patternList:
        if pattern.get('rhythmPattern') == newPattern.get('rhythmPattern'):
            return False
    # If the loop completes without finding a duplicate, add the new pattern
    return True


def rhythmPatterns(numerator, denominator):
    rhythm = str(denominator)
    rhythmPatternDictionary = []
    longToneRhythms = [{"rhythmPattern": [["1"]],
                        "timeSignature": (numerator, denominator),
                        "rhythm": "whole_note",
                        "articulation": [{"articulation": "fermata",
                                         "index": 0,
                                         "name": "fermata"}],
                        "dynamic": ""
                       },{
                        "rhythmPattern": [["1"], ["~"], ["1"]],
                        "timeSignature": (numerator, denominator),
                        "rhythm": "whole_note",
                        "articulation": [{"articulation": "fermata",
                                          "index": 0,
                                          "name": "fermata"
                                        },{
                                            "articulation": "fermata",
                                          "index": 1,
                                          "name": ""}
                                         ],
                        "dynamic": ""}]

    rhythmPatternDictionary.append({"rhythmType": "longTone",
                                    "rhythmPatterns": longToneRhythms})

    quarterNoteOneBarRhythms = [{"rhythmPattern": [["4"], ["4"], ["4"], ["4"]],
                                 "timeSignature": (numerator, denominator),
                                 "rhythm": "quarter note",
                                 "articulation": [],
                                 "dynamic": ""}]
    oneBarQuarterRests = [["r4"],["r4"],["r4"],["r4"]]

    # One pitch, 3 rests
    newPatterns=[]
    for i in range(numerator):
        oneBarQuarterNoteRhythm = oneBarQuarterRests.copy()
        oneBarQuarterNoteRhythm[i] = [rhythm]
        newPattern = {"rhythmPattern": oneBarQuarterNoteRhythm,
                     "timeSignature": (numerator, denominator),
                     "rhythm": "quarter note",
                     "articulation": [],
                     "dynamic": ""}
        if (noDuplicateRhythms(newPattern, quarterNoteOneBarRhythms)):
            quarterNoteOneBarRhythms.append(newPattern)


        # quarterNoteOneBarRhythms.append()
    i=0

    for i in range(numerator):
        newPatterns = []
        for j in range(1 + i, numerator):
            oneBarQuarterNoteRhythm = oneBarQuarterRests.copy()
            oneBarQuarterNoteRhythm[i] = ["4"]
            oneBarQuarterNoteRhythm[j] = ["4"]
            newPattern = {"rhythmPattern": oneBarQuarterNoteRhythm,
                          "timeSignature": (numerator, denominator),
                          "rhythm": "quarter note",
                          "articulation": [],
                          "dynamic": ""}
            if(noDuplicateRhythms(newPattern, quarterNoteOneBarRhythms)):
                newPatterns.append(newPattern)
        quarterNoteOneBarRhythms.extend(newPatterns)

    # for i in range(2, beats):
    #     oneBarQuarterNoteRhythm = oneBarQuarterRests.copy()
    #     oneBarQuarterNoteRhythm[1] = ["4"]
    #     oneBarQuarterNoteRhythm[i] = ["4"]
    #     newPattern = {"rhythmPattern": oneBarQuarterNoteRhythm,
    #                   "timeSignature": (4, 4),
    #                   "rhythm": "quarter note",
    #                   "articulation": [],
    #                   "dynamic": ""}
    #     noDuplicateRhythms(newPattern, quarterNoteOneBarRhythms)
        # quarterNoteOneBarRhythms.append({"rhythmPattern": oneBarQuarterNoteRhythm,
        #                                  "timeSignature": (4, 4),
        #                                  "rhythm": "quarter note",
        #                                  "articulation": [],
        #                                  "dynamic": ""})

    quarterNoteOneBarRhythms.append({"rhythmPattern": [["r4"], ["r4"], ["4"], ["4"]],
                                         "timeSignature": (numerator, denominator),
                                         "rhythm": "quarter note",
                                         "articulation": [],
                                         "dynamic": ""})

    oppositePatterns = []
    for pattern in quarterNoteOneBarRhythms:
        newPattern = []
        for r in pattern.get("rhythmPattern"):
            if r[0] == "4":
                newPattern.append(["r4"])
            elif r[0] == "r4":
                newPattern.append(["4"])
        oppositePatterns.append({"rhythmPattern": newPattern,
                                         "timeSignature": (4, 4),
                                         "rhythm": "quarter note",
                                         "articulation": [],
                                         "dynamic": ""})

    for newPattern in oppositePatterns:
        if (noDuplicateRhythms(newPattern, quarterNoteOneBarRhythms)):
            quarterNoteOneBarRhythms.append(newPattern)

    rhythmPatternDictionary.append({"rhythmType": "oneBarQuarterNote",
                                    "rhythmPatterns": quarterNoteOneBarRhythms,
                                    "meter": (numerator, denominator)})

    # 2 pitch, 2 rest patterns


    return rhythmPatternDictionary

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