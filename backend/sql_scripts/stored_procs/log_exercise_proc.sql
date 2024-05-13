USE Daily_Shed;
DROP PROCEDURE IF EXISTS log_exercise_proc;
DELIMITER //

CREATE PROCEDURE log_exercise_proc(
    IN sessionID_p   		INT,
    IN timestamp_p			DATE,
    IN sub_p				VARCHAR(45),
    IN exerciseID_p			INT,
    IN rating_p				INT,
    IN comment_p			VARCHAR(255)
)

BEGIN
        
    -- DECLARE sql_error BOOLEAN DEFAULT FALSE;
    DECLARE sql_error_code INT DEFAULT 0;
	DECLARE sql_error_message VARCHAR(255) DEFAULT '';
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
		BEGIN
			GET DIAGNOSTICS CONDITION 1
			@sql_error_message = MESSAGE_TEXT,
			@sql_error_code = MYSQL_ERRNO;
			ROLLBACK;
			SELECT @sql_error_code AS Error_Code, @sql_error_message AS Error_Message;
		END;

    START TRANSACTION;
    
		INSERT INTO ExerciseLog (exerciseID, timestamp, comment, rating, sub, sessionID)
        VALUES(exerciseID_p, timestamp_p, comment_p, rating_p, sub_p, sessionID_p);
		
    IF sql_error_code = 0 THEN
		SELECT 'Exercise logged' AS message;
		COMMIT;
	ELSE
		ROLLBACK;
		SELECT 'Transaction rolled back due to error:', sql_error_message AS Error_Message;
	END IF;
    
END //

DELIMITER ;

SELECT * FROM ExerciseLog;
DELETE FROM ExerciseLog;
SELECT * FROM users;
INSERT INTO ExerciseLog (exerciseID, timestamp, comment, rating, sub, sessionID)
VALUES(124, '2024-05-10T13:19:12.711Z', 'test', 1, '0b44c9de-c681-479d-8f89-e8af14a57458', 257);