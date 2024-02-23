from collections import Counter
from setDesigner.patternCollections import getCollection
from setDesigner.fetchExerciseDetails import fetchExerciseDetails
from setDesigner.directions import chooseDirection, descendingPattern, ascendingDescendingPattern, descendingAscendingPattern
import random

def getNewNotePattern(program, i):
    notePatternType = program.get('exerciseDetails')[i].get('notePatternType')
    collections = getCollection('notePattern')
    notePatternCollection = [
        pattern for collection in collections for pattern in collection['patterns'] if pattern.get('notePatternType') == notePatternType
    ]
    # Gets the next notePattern index for the player.
    for collection in program.get("collections"):
        if collection.get("notePatternType") == notePatternType:
            currentPlayerIndex = collection["index"]
            if currentPlayerIndex >= len(notePatternCollection):
                collection['index'] = -1
            else:
                collection['index'] = currentPlayerIndex + 1
            notePattern = notePatternCollection[
                ((int(currentPlayerIndex) + 1) )% len(notePatternCollection)
                ]
            notePattern['collectionTitle'] = collection.get('collectionTitle')
            return notePattern
    return None

def getNotePatternRhythmLength(pitches):
    if pitches.get('holdLastNote'):
        return len(pitches.get('notePattern')) - 1
    return len(pitches.get('notePattern'))

def getMinPlays(notePatternOptions):
    selectedExerciseCounts = Counter(
        notePattern.get('exercise').get('exerciseName') for notePattern in notePatternOptions
    )
    return selectedExerciseCounts[min(selectedExerciseCounts)]

def getReviewNotePattern(notePatternOptions, details, exerciseHistory):
    minPlays = getMinPlays(notePatternOptions)
    reviewPatterns = [
        exercise
        for exercise in exerciseHistory
        if exercise.get('playCount') == minPlays
           and exercise.get("rhythmMatcher") == details.get('rhythmMatcher')]

    reviewPattern = reviewPatterns[random.randint(0, len(reviewPatterns) - 1)]
    pattern = fetchExerciseDetails(reviewPattern).get('pitchPattern')

    if reviewPattern.get("notePatternType") != "single_note_long_tone":
        direction = chooseDirection(pattern, reviewPattern.get('directions'))
        if direction == "descending":
            return descendingPattern(pattern)
        elif direction == "ascending descending":
            return ascendingDescendingPattern(pattern)
        elif direction == "descending ascending":
            return descendingAscendingPattern(pattern)
    return pattern
