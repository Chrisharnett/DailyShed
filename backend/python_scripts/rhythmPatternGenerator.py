from objects.exerciseObjects import RhythmPattern


def noDuplicateRhythms(newPattern, patternList):
    for pattern in patternList:
        if pattern.getRhythmPattern == newPattern:
            return False
    # If the loop completes without finding a duplicate, add the new pattern
    return True

def singleNoteWholeToneRhythms(numerator, denominator):
    toneRhythmId = 0
    rhythmPatterns = []
    rhythmPatterns.append(
        RhythmPattern(
            "Single_note_long_tone_" + str(toneRhythmId),
            "tone",
            "one note long tone",
            [["1"]],
            (numerator, denominator),
            [{"articulation": "fermata", "index": 0, "name": "fermata"}],
        )
    )
    toneRhythmId += 1

    rhythmPatterns.append(
        RhythmPattern(
            "Single_note_long_tone_" + str(toneRhythmId),
            "tone",
            "one note long tone",
            [["1"], ["~"], ["1"]],
            (numerator, denominator),
            [
                {"articulation": "fermata", "index": 0, "name": "fermata"},
                {"articulation": "fermata", "index": 1, "name": ""},
            ],
        )
    )

    toneRhythmId += 1

    return rhythmPatterns


# TODO: Use rhythmPattern objects.
def quarterNoteRhythms(numerator, denominator):
    rhythm = str(denominator)
    rhythmId = 0
    rhythmPatterns = []

    rhythmPatterns.append(
        RhythmPattern(
            "r" + str(rhythmId),
            "Quarter Note",
            "quarter note",
            [["4"], ["4"], ["4"], ["4"]],
            (numerator, denominator),
        )
    )
    rhythmId += 1

    oneBarQuarterRests = [["r4"], ["r4"], ["r4"], ["r4"]]

    # One pitch, 3 rests
    for i in range(numerator):
        oneBarQuarterNoteRhythm = [["r4"], ["r4"], ["r4"], ["r4"]]
        oneBarQuarterNoteRhythm[i] = [rhythm]
        if noDuplicateRhythms(oneBarQuarterNoteRhythm, rhythmPatterns) == True:
            rhythmPatterns.append(
                RhythmPattern(
                    "r" + str(rhythmId),
                    "Quarter Note",
                    "quarter note",
                    oneBarQuarterNoteRhythm,
                    (numerator, denominator),
                )
            )
            rhythmId += 1

    for i in range(numerator):
        newPatterns = []
        for j in range(1 + i, numerator):
            oneBarQuarterNoteRhythm = oneBarQuarterRests.copy()
            oneBarQuarterNoteRhythm[i] = ["4"]
            oneBarQuarterNoteRhythm[j] = ["4"]
            if noDuplicateRhythms(oneBarQuarterNoteRhythm, rhythmPatterns) == True:
                rhythmPatterns.append(
                    RhythmPattern(
                        "r" + str(rhythmId),
                        "Quarter Note",
                        "quarter note",
                        oneBarQuarterNoteRhythm,
                        (numerator, denominator),
                    )
                )
                rhythmId += 1

    rhythmPatterns.append(
        RhythmPattern(
            "r" + str(rhythmId),
            "Quarter Note",
            "quarter note",
            [["r4"], ["r4"], ["4"], ["4"]],
            (numerator, denominator),
        )
    )
    rhythmId += 1

    oppositePatterns = []
    for pattern in rhythmPatterns:
        newPattern = []
        p = pattern.getRhythmPattern
        for r in p:
            if r == ["4"]:
                newPattern.append(["r4"])
            elif r == ["r4"]:
                newPattern.append(["4"])
        oppositePatterns.append(newPattern)

    for newPattern in oppositePatterns:
        if noDuplicateRhythms(newPattern, rhythmPatterns):
            rhythmPatterns.append(
                RhythmPattern(
                    "rhythm_" + str(rhythmId),
                    "Quarter Note",
                    "quarter note",
                    newPattern,
                    (numerator, denominator),
                )
            )
            rhythmId += 1

    return rhythmPatterns


def main():
    # Time signature. Numerator has to be int, denominator a string.
    numerator = 4
    denominator = "4"
    rhythms = []
    rhythms.extend(singleNoteWholeToneRhythms(numerator, denominator))
    rhythms.extend(quarterNoteRhythms(numerator, denominator))
    for pattern in rhythms:
        print(pattern.getRhythmPattern)


if __name__ == "__main__":
    main()
