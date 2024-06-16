USE Daily_Shed;
DROP PROCEDURE IF EXISTS clear_collections_and_exercises_proc;
DELIMITER //

CREATE PROCEDURE clear_collections_and_exercises_proc(

)
BEGIN
	DECLARE sql_error BOOLEAN DEFAULT FALSE;    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    
    START TRANSACTION;		
		DELETE FROM UserPracticeSessionExercises;
		DELETE FROM ProgramExercises;
		DELETE FROM UserRoutineExercises;
		DELETE FROM UserPrograms;
		DELETE FROM Programs;
		DELETE FROM Instruments;
		DELETE FROM scaleModes;
		DELETE FROM CollectionPatterns;
		DELETE FROM Collections;
		DELETE FROM ExerciseLog;
		DELETE FROM Exercises;
		DELETE FROM NotePatterns;
		DELETE FROM RhythmPatterns;
		DELETE FROM UserPracticeRoutines;
		DELETE FROM UserPracticeSession;
		DELETE FROM TonicSequences;
		DELETE FROM scalePatternTypes;
		DELETE FROM CollectionType;
        
	IF sql_error = FALSE THEN
		SELECT('Data removed') AS message;
        COMMIT;
    ELSE
		SELECT('ERROR, rollback') AS message;
        ROLLBACK;
    END IF;
END //


DELIMITER ;

CALL clear_collections_and_exercises_proc;

DELETE FROM UserPracticeSessionExercises;
DELETE FROM ProgramExercises;
DELETE FROM UserRoutineExercises;
DELETE FROM UserPrograms;
DELETE FROM Programs;
DELETE FROM Instruments;
DELETE FROM scaleModes;
DELETE FROM CollectionPatterns;
DELETE FROM Collections;
DELETE FROM ExerciseLog;
DELETE FROM Exercises;
DELETE FROM NotePatterns;
DELETE FROM RhythmPatterns;
DELETE FROM UserPracticeRoutines;
DELETE FROM UserPracticeSession;
DELETE FROM TonicSequences;
DELETE FROM scalePatternTypes;
DELETE FROM CollectionType;






 