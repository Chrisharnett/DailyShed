from setDesigner.rhythmPatterns import getMinPlays
from setDesigner.patternCollections import getCollection
from setDesigner.fetchExerciseDetails import fetchExerciseDetails
from setDesigner.directions import chooseDirection, descendingPattern, ascendingDescendingPattern, descendingAscendingPattern
import random

def getNotePatternCollection(collections, matcher):
    return [
        pattern for collection in collections for pattern in collection['patterns'] if pattern.get('notePatternType') == matcher
    ]

# def getNextNotePattern(interval, collection):
#     newIndex = interval['currentIndex']+1
#     # return notePattern from collection where notePattern is next in index % collection:Length
#     return interval
def getNextNotePattern(interval, collection):
    notePatternType = interval['notePatternType']
    program = None
    collections = getCollection('notePattern')
    notePatternCollection = getNotePatternCollection(collections, notePatternType)
    # Gets the next notePattern index for the player.
    for collection in program.get("collections"):
        if collection.get("notePatternType") == notePatternType:
            currentPlayerIndex = int(collection["index"])
            if currentPlayerIndex >= len(notePatternCollection):
                newIndex = int(collection['index']) + 1
                collection['index'] = newIndex
                return None, program
            else:
                collection['index'] = currentPlayerIndex + 1
            notePattern = notePatternCollection[
                ((int(currentPlayerIndex) + 1) ) % len(notePatternCollection)
                ]
            notePattern['collectionTitle'] = collection.get('collectionTitle')
            return notePattern, program
    return None

def getNotePatternRhythmLength(notePattern, holdLastNote):
    if holdLastNote:
        length = len((notePattern)) - 1
        return length
    length = len((notePattern))
    return length

def getReviewNotePattern(notePatternOptions, details, exerciseHistory):
    minPlays = getMinPlays(notePatternOptions)
    reviewPatterns = [
        exercise
        for exercise in exerciseHistory
        if exercise.get('playCount') == minPlays
           and exercise.get("rhythmMatcher") == details.get('rhythmMatcher')]

    reviewPattern = reviewPatterns[random.randint(0, len(reviewPatterns) - 1)]
    pattern = fetchExerciseDetails(reviewPattern).get('notePattern')

    if pattern.get("notePatternType") != "single_note_long_tone":
        direction = chooseDirection(reviewPattern.get('directions'))
        if direction == "descending":
            return descendingPattern(pattern)
        elif direction == "ascending descending":
            return ascendingDescendingPattern(pattern)
        elif direction == "descending ascending":
            return descendingAscendingPattern(pattern)
    return pattern
