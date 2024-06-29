USE Daily_Shed;
DROP PROCEDURE IF EXISTS reset_player_proc;
DELIMITER //

CREATE PROCEDURE reset_player_proc(
	IN sub_p	VARCHAR(45)
)
BEGIN
    DELETE FROM ExerciseLog WHERE sub = sub_p;
	DELETE FROM UserPracticeSessionExercises
	WHERE UserPracticeSessionID IN (
		SELECT UserPracticeSessionID
		FROM UserPracticeSession
		WHERE sub = sub_p
		);   
		
	DELETE FROM UserRoutineExercises 
	WHERE UserProgramID IN (
		SELECT UserProgramID
		FROM UserPrograms
		WHERE sub = sub_p
		);

	DELETE FROM UserPracticeRoutines WHERE sub = sub_p;

	DELETE FROM UserPracticeSession WHERE sub = sub_p;

	DELETE FROM UserPrograms WHERE sub = sub_p;
    
END //

DELIMITER ;

CALL reset_player_proc('0b44c9de-c681-479d-8f89-e8af14a57458');

DELETE FROM ExerciseLog WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
DELETE FROM UserPracticeSessionExercises
WHERE UserPracticeSessionID IN (
	SELECT UserPracticeSessionID
    FROM UserPracticeSession
    WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458'
    );   
    
DELETE FROM UserRoutineExercises 
WHERE UserProgramID IN (
	SELECT UserProgramID
    FROM UserPrograms
	WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458'
    );

DELETE FROM UserPracticeRoutines WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';

DELETE FROM UserPracticeSession WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';

DELETE FROM UserPrograms WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';


 