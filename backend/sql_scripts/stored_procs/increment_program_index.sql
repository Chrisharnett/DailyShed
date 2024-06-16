USE Daily_Shed;
DROP PROCEDURE IF EXISTS increment_program_index_proc;
DELIMITER //

CREATE PROCEDURE increment_program_index_proc(
	IN userProgramID_p	INT
)
BEGIN
	UPDATE UserPrograms
    SET currentIndex = currentIndex + 1
    WHERE userProgramID = userProgramID_p;
    
    SELECT currentIndex
    FROM UserPrograms
    WHERE userProgramID = userProgramID_p;
    
END //


DELIMITER ;

SELECT * FROM UserPrograms;
UPDATE UserPrograms
    SET currentIndex = -1
    WHERE userProgramID = 97;