USE Daily_Shed;
DROP PROCEDURE IF EXISTS reset_player_proc;
DELIMITER //

CREATE PROCEDURE reset_player_proc(
)
BEGIN
    DELETE FROM ExerciseLog;
    
    UPDATE UserPrograms
	SET scaleTonicIndex = 1;
    
    UPDATE UserPrograms
    SET currentIndex = -1;
    
    DELETE FROM UserPracticeSession;
    
END //

DELIMITER ;

CALL reset_player_proc;
SELECT * FROM Exercises;

SELECT * FROM UserPrograms;

DELETE FROM UserPracticeSessionExercises;
DELETE FROM ProgramExercises;
DELETE FROM Exercises;

 