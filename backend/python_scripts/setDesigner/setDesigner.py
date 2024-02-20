from setDesigner.notePatterns import getReviewNotePattern, getNewNotePattern, getRhythmLength
from setDesigner.rhythmPatterns import getNewRhythmPattern, getRhythmReviewPattern, getMinPlays, rhythmPatternNoteLength
from setDesigner.createExercise import createExercise
from setDesigner.patternCollections import getCollection

def setDesigner(player):
    program = player.get('program')
    exerciseDetails = player.get('program').get('exerciseDetails')
    previousSet = player.get('previousSet')
    exerciseHistory = player.get('exerciseMetadata')
    newSet = []

    for i in range(len(exerciseDetails)):
        if exerciseDetails[i].get('reviewBool') and previousSet:
            notePatternType = exerciseDetails[i].get('notePatternType')

            notePatternOptions = [
                exercise for exercise in exerciseHistory
                if exercise.get('notePatternType') == notePatternType
            ]
            pitches = getReviewNotePattern(notePatternOptions, exerciseDetails[i], exerciseHistory)
            rhythm = getNewRhythmPattern(
                getRhythmLength(pitches),
                [collection for collection in getCollection('rhythm') if
                 collection.get('collectionType') == 'rhythm' and
                 exerciseDetails[i].get('rhythmMatcher') == collection.get('title')]
            )
            newSet.append(createExercise(pitches, rhythm, exerciseDetails[i]))

        else:
            pitches = getNewNotePattern(program, i)
            if previousSet:
                # Get a review rhythm pattern for the collection type.
                possibleRhythms = []
                for exercise in exerciseHistory:
                    if (
                            exercise.get("rhythmMatcher")
                            == exerciseDetails[i].get('rhythmMatcher')
                    ):
                        possibleRhythms.append(exercise)
                if 0 < len(possibleRhythms):
                    minPlays = getMinPlays(possibleRhythms)
                    rhythm = getRhythmReviewPattern(
                        possibleRhythms, minPlays, getRhythmLength(pitches), exerciseDetails[i]
                    )
                else:
                    rhythm = getNewRhythmPattern(getRhythmLength(pitches), exerciseDetails[i]["rhythmMatcher"])
            else:
                rhythmCollections = getCollection('rhythm')
                matchingCollections = [collection for collection in rhythmCollections if
                                       exerciseDetails[i].get('rhythmMatcher') == collection.get('title')]
                rhythm = next(
                    pattern for collection in matchingCollections for pattern in collection['patterns']
                    if pattern.get('rhythmDescription') == exerciseDetails[i].get('rhythmMatcher')
                    and rhythmPatternNoteLength(pattern) == getRhythmLength(pitches)
                )

            e = createExercise(pitches, rhythm, exerciseDetails[i])
            newSet.append(e)
    return newSet