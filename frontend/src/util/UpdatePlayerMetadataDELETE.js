const updatePlayerMetadata = (playerDetails, exerciseMetadata) => {
  let exercises = playerDetails.exerciseMetadata.slice();

  let existingExercise = exercises.find(
    (ex) => ex.name === exerciseMetadata.exercise.name
  );

  if (existingExercise) {
    const newDirection = exerciseMetadata.exercise.direction;
    if (!existingExercise.directions.includes(newDirection)) {
      existingExercise.directions.push(newDirection);
    }

    existingExercise.notePatternRhythmLength =
      exerciseMetadata.exercise.notePatternRhythmLength;
    existingExercise.notePatternType =
      exerciseMetadata.exercise.notePatternType;
    existingExercise.rhythmMatcher = exerciseMetadata.exercise.rhythmMatcher;
    existingExercise.latestRating = exerciseMetadata.rating;
    existingExercise.latestComment = exerciseMetadata.comment;
    existingExercise.playCount = (existingExercise.playCount || 0) + 1;
    existingExercise.name = exerciseMetadata.exercise.name;
  } else {
    exercises.push({
      name: exerciseMetadata.exercise.name,
      notePatternRhythmLength:
        exerciseMetadata.exercise.notePatternRhythmLength,
      notePatternType: exerciseMetadata.exercise.notePatternType,
      rhythmMatcher: exerciseMetadata.exercise.rhythmMatcher,
      directions: [exerciseMetadata.exercise.direction],
      latestRating: exerciseMetadata.rating,
      latestComment: exerciseMetadata.comment,
      playCount: 1,
    });
  }

  return {
    ...playerDetails,
    exerciseMetadata: exercises,
  };
};

// export default updatePlayerMetadata;
