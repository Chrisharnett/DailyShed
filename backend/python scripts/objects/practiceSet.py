import random
from objects.exerciseObjects import Exercise, NotePattern, RhythmPattern
import math
from collections import Counter


class PracticeSet:
    def __init__(self, player, notePatternCollections, rhythmPatterns):
        self.__player = player
        self.__notePatternCollections = notePatternCollections
        self.__rhythmPatterns = rhythmPatterns

    def getExerciseCounts(self):
        return Counter(
            exercise["exercise"]["exerciseName"]
            for exercise in self.__player.exerciseHistory
        )

    # # TODO Make the min playcount account for type
    # def minPlayCount(self, matcher):
    #     if len(self.__player.exerciseHistory) == 0:
    #         return None
    #     # exerciseCounts = self.getExerciseCounts()
    #     #
    #     # # Filter exercises where 'rhythmMatcher' matches the specified matcher
    #     # matchingExercises = {exercise['description']: exerciseCounts[exercise['description']]
    #     #                       for exercise in self.__player.exerciseHistory
    #     #                       if exercise['exercise'].getPitchPattern()['rhythmMatcher'] == matcher}
    #     #
    #     # if matchingExercises:
    #     #     minExercise = min(matchingExercises, key=matchingExercises.get)
    #     #     return minExercise, matchingExercises[minExercise]
    #     # else:
    #     #     return None
    #
    #     return min([exercise for exercise in self.__player.exerciseHistory if
    #                exercise['exercise'].getPitchPattern['rhythmMatcher'] == type],
    #                key=lambda x: x.getPlayCount).getPlayCount

    def chooseDirection(self, notePattern):
        directions = [
            "ascending",
            "descending",
            "ascending descending",
            "descending ascending",
        ]
        uniqueDirections = set()
        reviewedDirections = [
            x["exercise"]["pitchPattern"]["direction"]
            for x in self.__player.exerciseHistory
            if x["exercise"]["pitchPattern"] == notePattern
        ]
        index = len(reviewedDirections) - 1
        if 0 < index < 4:
            return directions[index]
        return directions[random.randint(0, len(directions) - 1)]

    def descendingPattern(self, pattern):
        d = pattern["notePattern"].copy()
        d.reverse()
        return NotePattern(
            f"{pattern['notePatternId']}ad",
            pattern["notePatternType"],
            d,
            pattern["rhythmMatcher"],
            f"from the {pattern['notePattern'][-1]}",
            "descending",
            pattern["repeatMe"],
            pattern["holdLastNote"],
        )

    def ascendingDescendingPattern(self, pattern):
        a = pattern["notePattern"].copy()
        d = pattern["notePattern"].copy()
        d.reverse()
        a.pop()
        a.extend(d)
        return NotePattern(
            f"{pattern['notePatternId']}ad",
            pattern["notePatternType"],
            a,
            pattern["rhythmMatcher"],
            f"to the {pattern['notePattern'][-1]}",
            "ascending descending",
            pattern["repeatMe"],
            pattern["holdLastNote"],
        )

    def descendingAscendingPattern(self, pattern):
        d = pattern["notePattern"].copy()
        d.reverse()
        d.pop()
        d.extend(pattern["notePattern"])
        return NotePattern(
            f"{pattern['notePatternId']}da",
            pattern["notePatternType"],
            d,
            pattern["rhythmMatcher"],
            f"from the {pattern['notePattern'][-1]}",
            "descending ascending",
            pattern["repeatMe"],
            pattern["holdLastNote"],
        )

    def maxRhythmNoteLength(self, rhythms):
        return (max(rhythms, key=lambda x: x.noteLength)).noteLength

    def multipleBarRhythm(self, rhythms, length):
        # be aware of last note
        # Get the minimum number of bars using % ()
        maxRhythmLength = self.maxRhythmNoteLength(rhythms)
        minimumNumberOfMeasures = math.ceil(length / maxRhythmLength)
        measureNumber = 0
        remainder = length
        r = []
        id = ""
        while remainder > maxRhythmLength:
            # Get the rhythms that are at least length/minNumberOfMesures
            possibleRhythms = [
                x for x in rhythms if length / minimumNumberOfMeasures <= x.noteLength
            ]
            if len(possibleRhythms) > 1:
                measure = possibleRhythms[random.randint(0, len(possibleRhythms) - 1)]
            else:
                measure = possibleRhythms[0]
            r.extend(measure.getRhythmPattern)
            id += measure.getRhythmPatternId
            remainder -= measure.noteLength
        possibleRhythms = [x for x in rhythms if x.noteLength == remainder]
        lastMeasure = possibleRhythms[random.randint(0, len(possibleRhythms) - 1)]
        r.extend(lastMeasure.getRhythmPattern)
        id += lastMeasure.getRhythmPatternId
        rhythmPattern = RhythmPattern(
            id,
            lastMeasure.getRhythmType,
            lastMeasure.getRhythmDescription,
            r,
            lastMeasure.getTimeSignature,
            lastMeasure.getArticulation,
        )
        return rhythmPattern

    def getNoteReviewPattern(self, type):
        # Get a list of all notePatterns of the same type
        notePatternOptions = []
        for playerExercise in self.__player.exerciseHistory:
            if playerExercise["exercise"]["pitchPattern"]["rhythmMatcher"] == type:
                notePatternOptions.append(playerExercise)

        minPlays = self.getMinPlays(notePatternOptions)
        # Get counts for all exercises
        exerciseCounts = self.getExerciseCounts()

        # Get a list of pitchPatterns from exerciseHistory that
        #   have been played minPlay # of times
        #   match the rhythmMatcher Type
        #   Gotta figure out the last bit, but it works.
        reviewPatterns = [
            playerExercise["exercise"]["pitchPattern"]
            for playerExercise in self.__player.exerciseHistory
            if exerciseCounts[playerExercise["exercise"]["exerciseName"]] == minPlays
            and playerExercise["exercise"]["pitchPattern"]["rhythmMatcher"] == type
            and (
                isinstance(
                    playerExercise["exercise"]["pitchPattern"]["notePatternId"],
                    (int, str),
                )
                and str(
                    playerExercise["exercise"]["pitchPattern"]["notePatternId"]
                ).isdigit()
            )
        ]
        reviewPattern = reviewPatterns[random.randint(0, len(reviewPatterns) - 1)]
        if reviewPattern["notePatternType"] != "tone":
            direction = self.chooseDirection(reviewPattern)
            if direction == "descending":
                return self.descendingPattern(reviewPattern)
            elif direction == "ascending descending":
                return self.ascendingDescendingPattern(reviewPattern)
            elif direction == "descending ascending":
                return self.descendingAscendingPattern(reviewPattern)
        return NotePattern(
            reviewPattern["notePatternId"],
            reviewPattern["notePatternType"],
            reviewPattern["notePattern"],
            reviewPattern["rhythmMatcher"],
            reviewPattern["description"],
            reviewPattern["dynamic"],
            reviewPattern["direction"],
            reviewPattern["repeatMe"],
            reviewPattern["holdLastNote"],
        )

    def getRhythmReviewPattern(self, possibleRhythms, min, length):
        rhythms = []
        exerciseCounts = self.getExerciseCounts()
        for rhythm in possibleRhythms:
            if (
                exerciseCounts[rhythm["exercise"]["exerciseName"]] == min
                and rhythm["exercise"]["rhythmPattern"]["noteLength"] == length
            ):
                rhythms.append(rhythm["exercise"]["rhythmPattern"])
        if len(rhythms) == 0:
            rhythms = [
                self.getNewRhythmPattern(
                    possibleRhythms[0]["exercise"]["pitchPattern"]["rhythmMatcher"],
                    length,
                )
            ]
            return rhythms[random.randint(0, len(rhythms) - 1)]
        r = rhythms[random.randint(0, len(rhythms) - 1)]
        return RhythmPattern(
            r["rhythmId"],
            r["rhythmType"],
            r["rhythmDescription"],
            r["rhythmPattern"],
            r["timeSignature"],
            r["articulation"],
        )

    def getNewNotePattern(self, type):
        notePatternCollection = next(
            x for x in self.__notePatternCollections if x.getName == type
        )
        currentPlayerIndex = self.__player.getCurrentStatus["currentIndex"][type][
            "index"
        ]

        pitches = notePatternCollection.getPatterns[
            (currentPlayerIndex + 1) % len(notePatternCollection.getPatterns)
        ]

        if currentPlayerIndex >= len(notePatternCollection.getPatterns):
            self.__player.setIndex(type, -1)
        else:
            self.__player.setIndex(type, currentPlayerIndex + 1)

        return pitches

    def getNewRhythmPattern(self, type, length):
        rhythmsThatFit = [
            x for x in self.__rhythmPatterns.getPatterns if x.getRhythmType == type
        ]
        max = self.maxRhythmNoteLength(rhythmsThatFit)
        if max >= length:
            return next(x for x in rhythmsThatFit if x.noteLength == length)
        return self.multipleBarRhythm(rhythmsThatFit, length)

    def getMinPlays(self, exercises):
        selectedExerciseCounts = Counter(
            exercise["exercise"]["exerciseName"] for exercise in exercises
        )
        return selectedExerciseCounts[min(selectedExerciseCounts)]

    def getNextSet(self):
        currentSetPattern = self.__player.getSetPattern
        newSet = []
        # set the length of the new set with None values
        for n in range(len(currentSetPattern)):
            newSet.append(None)

            #  Review lessons have a notePattern from the history with a new or random rhythm.
            #  Non-review exercises have a new notePattern with a rhythm from history.
        previousSet = self.__player.getPreviousSet

        for i in range(len(newSet)):
            # Build review exercise
            if currentSetPattern[i].get("reviewBool") and previousSet:
                pitches = self.getNoteReviewPattern(
                    previousSet[i]["pitchPattern"]["rhythmMatcher"]
                )
                rhythm = self.getNewRhythmPattern(
                    previousSet[i]["pitchPattern"]["rhythmMatcher"],
                    pitches.getRhythmLength(),
                )

                ex = Exercise(pitches, rhythm)
                newSet[i] = ex
            else:
                # Get the next note Pattern for the collection type
                pitches = self.getNewNotePattern(currentSetPattern[i].get("type"))
                if previousSet:
                    # Get a review rhythm pattern for the collection type.
                    possibleRhythms = []
                    for ex in self.__player.exerciseHistory:
                        if (
                            ex["exercise"]["rhythmPattern"]["rhythmType"]
                            == pitches.getRhythmMatcher
                        ):
                            possibleRhythms.append(ex)
                    minPlays = self.getMinPlays(possibleRhythms)

                    # minPlays = min(possibleRhythms, key=lambda x: x.get('playCount')).get('playCount')

                    rhythm = self.getRhythmReviewPattern(
                        possibleRhythms, minPlays, pitches.getRhythmLength()
                    )
                else:
                    rhythm = next(
                        pattern
                        for pattern in self.__rhythmPatterns.getPatterns
                        if pattern.getRhythmType == pitches.getRhythmMatcher
                        and pattern.noteLength == pitches.getRhythmLength()
                    )

                ex = Exercise(pitches, rhythm)
                newSet[i] = ex

        return newSet
