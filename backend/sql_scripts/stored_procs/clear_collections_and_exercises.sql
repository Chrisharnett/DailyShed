USE Daily_Shed;
DROP PROCEDURE IF EXISTS clear_collections_and_exercises_proc;
DELIMITER //

CREATE PROCEDURE clear_collections_and_exercises_proc(

)
BEGIN
	DELETE FROM UserPracticeSessionExercises;
	DELETE FROM ProgramExercises;
	DELETE FROM Exercises;
	DELETE FROM UserRoutineExercises;
	DELETE FROM UserPrograms;
	DELETE FROM Programs;
	DELETE FROM CollectionPatterns;
	DELETE FROM Collections;
	DELETE FROM NotePatterns;
	DELETE FROM RhythmPatterns;
    
END //


DELIMITER ;

CALL clear_collections_and_exercises_proc;
CALL clearUsers;

SELECT * FROM CollectionPatterns;
SELECT * FROM Collections;
SELECT * FROM ExerciseLog;
SELECT * FROM Exercises;
SELECT * FROM NotePatterns;
SELECT * FROM TonicSequences;
SELECT * FROM ProgramExercises;
SELECT * FROM Programs;
SELECT * FROM RhythmPatterns;
SELECT * FROM scaleModes;
SELECT * FROM UserPracticeRoutines;
SELECT * FROM UserPracticeSession;
SELECT * FROM UserPracticeSessionExercises;
SELECT * FROM UserPrograms;
SELECT * FROM UserRoutineExercises;
SELECT * FROM users;

DELETE FROM pitchNames;
DELETE FROM scaleModes;





 