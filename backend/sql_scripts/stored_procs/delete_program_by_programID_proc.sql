USE Daily_Shed;
DROP PROCEDURE IF EXISTS delete_program_by_programID_proc;

DELIMITER //

CREATE PROCEDURE delete_program_by_programID_proc (
    IN programID_p           INT
)
BEGIN 
	DECLARE sql_error BOOLEAN DEFAULT FALSE;  
        
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            SET sql_error = TRUE;
        END;
    
    START TRANSACTION;

        DELETE FROM UserPrograms WHERE programID = programID_p;
        DELETE FROM Programs WHERE programId = programID_p;

    IF sql_error = FALSE THEN
        COMMIT;
        SELECT 'Transaction Committed' AS debug_message;
    ELSE
        ROLLBACK;
        SELECT 'Transaction Rolled Back' AS debug_message;
    END IF;

END //

DELIMITER ;

CALL delete_program_by_programID_proc(512);