USE Daily_Shed;
DROP PROCEDURE IF EXISTS new_user_practice_routine_proc;
DELIMITER //

CREATE PROCEDURE new_user_practice_routine_proc(
    IN sub_p		VARCHAR(45),
    IN rounds_p		INT
)

BEGIN
	DECLARE newPracticeRoutineID_p			INT;
    DECLARE message							VARCHAR(255);
    DECLARE sql_error 						BOOLEAN DEFAULT FALSE;    
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;

    START TRANSACTION;
		UPDATE UserPracticeRoutines
        SET isActive = false
        WHERE sub = sub_p;
        
        INSERT INTO UserPracticeRoutines (sub, rounds, isActive) VALUES (sub_p, rounds_p, true);
        
        SET newPracticeRoutineID_p = LAST_INSERT_ID();        
        
		IF sql_error = FALSE THEN
            SELECT newPracticeRoutineID_p AS newRoutineID;
			COMMIT;
		ELSE
			SELECT 'Some bizarre error' AS message;
			ROLLBACK;
		END IF;
END //

DELIMITER ;

SELECT * FROM users;

CALL new_user_practice_routine_proc('0b44c9de-c681-479d-8f89-e8af14a57458', 12);


