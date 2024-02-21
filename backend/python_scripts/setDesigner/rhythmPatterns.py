import random
import math
from collections import Counter
from setDesigner.fetchExerciseDetails import fetchExerciseDetails

def getNewRhythmPattern(length, rhythmCollection):
    maxRhythmLength = max(rhythmPatternNoteLength(rhythmPattern) for collection in rhythmCollection for rhythmPattern in collection['patterns'])
    exactMatchRhythms = [rhythmPattern for collection in rhythmCollection for rhythmPattern in collection['patterns'] if rhythmPatternNoteLength(rhythmPattern) == length]
    if exactMatchRhythms:
        selectedRhythm = random.choice(exactMatchRhythms)
        return selectedRhythm
    else:
        return multipleBarRhythm(maxRhythmLength, rhythmCollection, length)

def getRhythmReviewPattern(possibleRhythms, min, length, exerciseDetails):
    rhythms = []
    for rhythm in possibleRhythms:
        if (
            rhythm.get("playCount") == min
            and rhythm.get("noteLength") == length
        ):
            rhythms.append(rhythm)
    if len(rhythms) == 0:
        rhythms = [
            getNewRhythmPattern(
                length,
                [collection for collection in getCollection('rhythm') if
                 collection.get('collectionType') == 'rhythm' and
                 exerciseDetails.get('rhythmMatcher') == collection.get('title')]
            )
        ]
        return rhythms[random.randint(0, len(rhythms) - 1)]
    r = fetchExerciseDetails(rhythms([random.randint(0, len(rhythms) - 1)])).get('rhythmPattern')
    return r

def rhythmPatternNoteLength(rhythmPattern):
    count = 0
    for r in rhythmPattern.get('rhythmPattern'):
        for n in r:
            if n.isdigit():
                count += 1
    n = sum(sublist.count("~") for sublist in rhythmPattern)
    count -= n
    return count

def multipleBarRhythm(maxRhythmLength, rhythms, length):
    minimumNumberOfMeasures = math.ceil(length / maxRhythmLength)
    measureNumber = 0
    remainder = length
    r = []
    id = ""
    while remainder > maxRhythmLength:
        possibleRhythms = [
            rhythmPattern for pattern in rhythms for rhythmPattern in pattern['patterns'] if length / minimumNumberOfMeasures <= rhythmPatternNoteLength(rhythmPattern)
        ]
        if len(possibleRhythms) > 1:
            measure = possibleRhythms[random.randint(0, len(possibleRhythms) - 1)]
        else:
            measure = possibleRhythms[0]

        r.extend(measure.get('rhythmPattern'))
        id += str(measure.get('rhythmPatternId'))
        remainder -= rhythmPatternNoteLength(measure)
    possibleRhythms = [rhythmPattern for pattern in rhythms for rhythmPattern in pattern['patterns'] if rhythmPatternNoteLength(rhythmPattern) == remainder]
    lastMeasure = possibleRhythms[random.randint(0, len(possibleRhythms) - 1)]
    r.extend(lastMeasure.get('rhythmPattern'))
    id += f"#{str(lastMeasure.get('rhythmPatternId'))}"
    rhythmPattern = rhythms[0].get('patterns')[0]
    rhythmPattern['rhythmPattern'] = r
    rhythmPattern['rhythmPatternId'] = id
    return rhythmPattern

def getMinPlays(notePatternOptions):
    selectedExerciseCounts = Counter(
        notePattern.get('exercise').get('exerciseName') for notePattern in notePatternOptions
    )
    return selectedExerciseCounts[min(selectedExerciseCounts)]
