USE Daily_Shed;
DROP PROCEDURE IF EXISTS update_user_session_proc;
DELIMITER //

CREATE PROCEDURE update_user_session_proc(
    IN userPracticeRoutineID_p		INT,
    IN userProgramID_p  			INT,
    IN reviewExercise_p				TINYINT
)

BEGIN
	DECLARE sub_p			INT;
    DECLARE message			VARCHAR(255);
    DECLARE sql_error 		BOOLEAN DEFAULT FALSE;    
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;

    START TRANSACTION;
		SELECT sub
        INTO sub_p
        FROM UserPracticeRoutines
        WHERE UserPracticeRoutineID = userPracticeRoutine_p;
        
		INSERT INTO UserRoutineExercises (userPracticeRoutineID, UserProgramID, reviewExercise)
        VALUES (userPracticeRoutineID_p, UserProgramID_p, reviewExercise_p);
        
		IF sql_error = FALSE THEN
            SELECT 'session updated' AS Message;
			COMMIT;
		ELSE
			SELECT message AS message;
			ROLLBACK;
		END IF;
END //

DELIMITER ;
