USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_new_user_proc;
DELIMITER //

CREATE PROCEDURE add_new_user_proc(
    IN sub         VARCHAR(45),
    IN email       VARCHAR(45),
    IN name        VARCHAR(45)
)
BEGIN
    
    DECLARE sql_error BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		SET sql_error = TRUE;

    START TRANSACTION;   
        INSERT INTO users (sub, email, userName) VALUES (sub, email, name);
		-- Check if user insertion was successful
		IF ROW_COUNT() > 0 THEN
			CALL add_default_program_proc('major_scale_to_the_ninth', 'major_single_note_long_tone', 'saxophone', sub);
		ELSE
			SELECT('1') AS message;
			SET sql_error = TRUE;
		END IF;

    IF sql_error = TRUE THEN
        SELECT message;
        ROLLBACK;
    ELSE
		SELECT('User added')
        COMMIT;
    END IF;
END //

DELIMITER ;

INSERT INTO users (sub, email, userName) VALUES ('534', 'testemail','testname');

CALL add_new_user_proc('5578h', 'testemail','testname');

SELECT* FROM  UserPrograms;
SELECT * FROM users;
UPDATE UserPrograms
SET scaleTonicIndex = 1 
WHERE scaleTonicIndex = 0;
 