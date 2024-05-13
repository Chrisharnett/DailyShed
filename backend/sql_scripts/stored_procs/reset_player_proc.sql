USE Daily_Shed;
DROP PROCEDURE IF EXISTS reset_player_proc;
DELIMITER //

CREATE PROCEDURE reset_player_proc(
)
BEGIN
    DELETE FROM ExerciseLog;
    
    
END //

DELIMITER ;

CALL clear_exercises_proc;
SELECT * FROM Exercises;

DELETE FROM UserPracticeSessionExercises;
DELETE FROM ProgramExercises;
DELETE FROM Exercises;

 