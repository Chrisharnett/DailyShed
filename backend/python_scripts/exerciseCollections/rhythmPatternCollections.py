import math
import copy

def rhythmPatternNoteLength(rhythmPattern):
    count = 0
    for r in rhythmPattern:
        for n in r:
            if isinstance(n, int) or n.isdigit():
                count += 1
    n = sum(sublist.count("~") for sublist in rhythmPattern)
    count -= n
    return count

def noDuplicateRhythms(newPattern, patternList):
    for pattern in patternList:
        if pattern.get('rhythmPattern') == newPattern:
            return False
    # If the loop completes without finding a duplicate, add the new pattern
    return True

def singleNoteWholeToneRhythms(numerator, denominator):
    toneRhythmId = 0
    rhythmPatterns = []
    pattern = [["1"]]
    rhythmPatterns.append({
        'rhythmPatternID': str(toneRhythmId),
        'rhythmDescription': "single_note_long_tone_rhythms",
        'rhythmPattern': pattern,
        'rhythmLength' : rhythmPatternNoteLength(pattern),
        'timeSignature': (numerator, denominator),
        'articulation': [{"articulation": "fermata", "index": 0, "name": "fermata"}],
        'measureLength': 1
    }
    )
    toneRhythmId += 1

    pattern = [["1"], ["~"], ["1"]]
    rhythmPatterns.append(
        {
            'rhythmPatternID': str(toneRhythmId),
            'rhythmDescription': "single_note_long_tone_rhythms",
            'rhythmPattern': pattern,
            'rhythmLength': rhythmPatternNoteLength(pattern),
            'timeSignature': (numerator, denominator),
            'articulation': [
                # {"articulation": "fermata", "index": 0, "name": "fermata"},
                # {"articulation": "fermata", "index": 1, "name": ""}
            ],
            'measureLength': 1
        }
    )
    toneRhythmId += 1

    return rhythmPatterns, len(rhythmPatterns)

def fillBar(element, numerator):
    bar = []
    for i in range(numerator):
        if (element[0] == 'r'):
            rhythm = int(element[1:])
        else:
            rhythm = int(element)
        for j in range(math.floor(rhythm/numerator)):
            bar.append([element])
    return bar

def oneBarOfRhythm(numerator, denominator, note):
    oneBarOfRhythm = fillBar(denominator, numerator)
    return oneBarOfRhythm

def eighthAndQuarterRhythms(numerator, denominator):
    rhythmID = 0
    rhythmPatterns = []
    eighthBeat =[]
    division = int(8/int(denominator))

    oneBarOfBeats = fillBar(denominator, numerator)
    eighthAndRest = ['8', 'r8']
    # all combinations of beats and 1 beat of eighths
    for i, beat in enumerate(oneBarOfBeats):
        for r in eighthAndRest:
            newRhythm = oneBarOfBeats.copy()
            newRhythm[i] = [r]
            for j in range(division - 1):
                newRhythm.insert(j+i+1, ['8'])
            if noDuplicateRhythms(newRhythm, rhythmPatterns):
                rhythmPatterns.append(
                    {
                    'rhythmPattern': newRhythm,
                    'rhythmPatternID': str(rhythmID),
                    'rhythmDescription': "eighth-note",
                    'rhythmLength': rhythmPatternNoteLength(newRhythm),
                    'timeSignature': (int(numerator), int(denominator)),
                    'articulation': None,
                    'measureLength': 1
                    })
                rhythmID += 1
            if division != 1:
                for k, beat in enumerate(oneBarOfBeats):
                    newIndex = (k+division+i)
                    if newIndex <= len(oneBarOfBeats):
                        twoEighthPairs = newRhythm.copy()
                        twoEighthPairs[newIndex] = ['8']
                        for j in range(division - 1):
                            twoEighthPairs.insert(newIndex + 1, ['8'])
                        if noDuplicateRhythms(twoEighthPairs, rhythmPatterns):
                            rhythmPatterns.append(
                                {
                                    'rhythmPattern': twoEighthPairs,
                                    'rhythmPatternID': str(rhythmID),
                                    'rhythmDescription': "eighth-note",
                                    'rhythmLength': rhythmPatternNoteLength(twoEighthPairs),
                                    'timeSignature': (numerator, denominator),
                                    'articulation': None,
                                    'measureLength': 1
                                })
                            rhythmID += 1
    oneBarOfEights = fillBar('8', numerator)
    rhythmPatterns.append(
        {
        'rhythmPattern': oneBarOfEights,
        'rhythmPatternID': str(rhythmID),
        'rhythmDescription': "eighth-note",
        'rhythmLength': rhythmPatternNoteLength(oneBarOfEights),
        'timeSignature': (numerator, denominator),
        'articulation': None,
        'measureLength': 1
        })
    for i, eighth in enumerate(oneBarOfEights):
        if i % 2 == 0:
            newRhythm = oneBarOfEights.copy()
            newRhythm[i] = ['r8']
            rhythmPatterns.append(
                {
                    'rhythmPattern': newRhythm,
                    'rhythmPatternID': str(rhythmID),
                    'rhythmDescription': "eighth-note",
                    'rhythmLength': rhythmPatternNoteLength(newRhythm),
                    'timeSignature': (numerator, denominator),
                    'articulation': None,
                    'measureLength': 1
                })
            rhythmID += 1

    return rhythmPatterns, len(rhythmPatterns)

def quarterNoteAndRestRhythms(numerator, denominator):
    # rhythm = str(denominator)
    rhythmId = 0
    rhythmPatterns = []
    rest = 'r4'
    barOfQuarters = fillBar(denominator, numerator)

    rhythmPatterns.append({
        'rhythmPatternID': str(rhythmId),
        'rhythmDescription': "quarter_note",
        'rhythmPattern': barOfQuarters,
        'rhythmLength': rhythmPatternNoteLength(barOfQuarters),
        'timeSignature': (numerator, denominator),
        'articulation': None,
        'measureLength': 1
    }
    )
    rhythmId += 1

    # One pitch, 3 rests
    for i in range(numerator):
        quarterAndRestRhythms = copy.deepcopy(barOfQuarters)
        for j, note in enumerate(barOfQuarters):
            quarterAndRestRhythms[j][0] = rest

        quarterAndRestRhythms[i] = [denominator]
        if noDuplicateRhythms(quarterAndRestRhythms, rhythmPatterns) == True:
            rhythmPatterns.append(
                {
                    'rhythmPatternID': str(rhythmId),
                    'rhythmDescription': "quarter_note",
                    'rhythmPattern': quarterAndRestRhythms,
                    'rhythmLength': rhythmPatternNoteLength(quarterAndRestRhythms),
                    'timeSignature': (numerator, denominator),
                    'articulation': None,
                    'measureLength': 1
                }
            )
            rhythmId += 1

    for i in range(numerator):
        newPatterns = []
        for j in range(1 + i, numerator):
            quarterAndRestRhythms = fillBar(rest, numerator)
            quarterAndRestRhythms[i] = [denominator]
            quarterAndRestRhythms[j] = [denominator]
            if noDuplicateRhythms(quarterAndRestRhythms, rhythmPatterns) == True:
                rhythmPatterns.append(
                    {
                        'rhythmPatternID': str(rhythmId),
                        'rhythmDescription': "quarter_note",
                        'rhythmPattern': quarterAndRestRhythms,
                        'rhythmLength': rhythmPatternNoteLength(quarterAndRestRhythms),
                        'timeSignature': (numerator, denominator),
                        'articulation': None,
                        'measureLength': 1
                    }
                )
                rhythmId += 1

    oppositePatterns = []
    for barOfQuarters in rhythmPatterns[1:]:
        newPattern = []
        p = barOfQuarters.get('rhythmPattern')
        for r in p:
            if r == [denominator]:
                newPattern.append([rest])
            elif r == [rest]:
                newPattern.append([denominator])
        oppositePatterns.append(newPattern)

    for newPattern in oppositePatterns:
        if noDuplicateRhythms(newPattern, rhythmPatterns):
            rhythmPatterns.append(
                {
                    'rhythmPatternID': str(rhythmId),
                    'rhythmDescription': "quarter_note",
                    'rhythmPattern': newPattern,
                    'rhythmLength': rhythmPatternNoteLength(newPattern),
                    'timeSignature': (numerator, denominator),
                    'articulation': None,
                    'measureLength': 1
                }
            )
            rhythmId += 1

    return rhythmPatterns, len(rhythmPatterns)

def main():
    # Time signature. Numerator has to be int, denominator a string.
    numerator = int(4)
    denominator = "4"
    rhythms = []
    # rhythms.extend(singleNoteWholeToneRhythms(numerator, denominator))
    # rhythms.extend(quarterNoteAndRestRhythms(numerator, denominator))
    rhythms.extend(eighthAndQuarterRhythms(numerator, denominator))
    for pattern in rhythms:
        print(pattern.get('rhythmPattern'))

if __name__ == "__main__":
    main()
