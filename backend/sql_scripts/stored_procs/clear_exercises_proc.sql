USE Daily_Shed;
DROP PROCEDURE IF EXISTS clear_exercises_proc;
DELIMITER //

CREATE PROCEDURE clear_exercises_proc(

)
BEGIN
	DELETE FROM UserPracticeSessionExercises;
	DELETE FROM ProgramExercises;
	DELETE FROM Exercises;
END //


DELIMITER ;


 