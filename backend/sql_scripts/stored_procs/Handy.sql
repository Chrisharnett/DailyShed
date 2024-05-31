-- TABLES
SELECT * FROM Exercises;
SELECT * FROM CollectionPatterns;

SELECT * FROM ExerciseLog;
SELECT * FROM Exercises;

SELECT * FROM pitchNames;
SELECT * FROM ProgramExercises;

SELECT * FROM UserPracticeRoutines;
SELECT * FROM UserPracticeSession;
SELECT * FROM UserPracticeSessionExercises;
SELECT * FROM UserPrograms;
SELECT * FROM UserRoutineExercises;
SELECT * FROM users;


SELECT * FROM NotePatterns;
SELECT * FROM RhythmPatterns;
SELECT * FROM Instruments;
SELECT * FROM TonicSequences;
SELECT * FROM Programs;
SELECT * FROM scaleModes;
SELECT * FROM Collections;
SELECT * FROM scalePatternTypes;

CALL clear_collections_and_exercises_proc();

-- VIEWS
SELECT * FROM get_practice_session;

-- STORED PROCS
CALL clear_collections_and_exercises_proc();

CALL clear_exercises_proc();
CALL reset_player_proc();

DELETE FROM UserPracticeSession;