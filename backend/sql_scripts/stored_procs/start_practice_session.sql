USE Daily_Shed;
DROP PROCEDURE IF EXISTS start_practice_session;
DELIMITER //

CREATE PROCEDURE start_practice_session(
    IN sub_p				VARCHAR(45)
)

BEGIN
    
    DECLARE sql_error BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;

    START TRANSACTION;
		INSERT INTO UserPracticeSession (sub) VALUES (sub_p);
    
		SELECT LAST_INSERT_ID;
    
END //

DELIMITER ;