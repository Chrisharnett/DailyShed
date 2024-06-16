USE Daily_Shed;
DROP PROCEDURE IF EXISTS clear_exercises_proc;
DELIMITER //

CREATE PROCEDURE clear_exercises_proc(

)
BEGIN
	DELETE FROM UserPracticeSessionExercises;
	DELETE FROM ProgramExercises;
    DELETE FROM ExerciseLog;
	DELETE FROM Exercises;
END //


DELIMITER ;

CALL clear_exercises_proc;
SELECT * FROM Exercises;

DELETE FROM UserPracticeSessionExercises;
DELETE FROM ProgramExercises;
DELETE FROM Exercises;

 