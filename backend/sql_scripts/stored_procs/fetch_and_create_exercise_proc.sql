USE Daily_Shed;
DROP PROCEDURE IF EXISTS fetch_and_create_exercise_proc;
DELIMITER //

CREATE PROCEDURE fetch_and_create_exercise_proc(
    IN notePatternID_p   	INT,
    IN rhythmPatternID_p	INT,
    IN tonic_p				VARCHAR(10),
    IN mode_p				VARCHAR(25),
    IN directionIndex_p		INT,
    IN programID_p			INT
)

BEGIN
    DECLARE exerciseID_p 	INT DEFAULT NULL;
    
    DECLARE sql_error BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;

    START TRANSACTION;
		SELECT exerciseID INTO exerciseID_p
		FROM Exercises
		WHERE notePatternID = notePatternID_p AND 
			rhythmPatternID = rhythmPatternID_p AND
            tonic = tonic_p AND
            mode = mode_p AND
            directionIndex = directionIndex_p
            ;

    IF exerciseID_p IS NOT NULL THEN
        SELECT exerciseID_p AS ExerciseID;
    ELSE
        CALL add_new_exercise_proc(notePatternID_p, rhythmPatternID_p, tonic_p, mode_p, directionIndex_p, programID_p);
        SELECT LAST_INSERT_ID() INTO exerciseID_p;
	END IF;
    
    IF sql_error = FALSE THEN
		SELECT exerciseID_p AS ExerciseID;
        COMMIT;
    ELSE
		SELECT('ERROR, rollback') AS message;
        ROLLBACK;
    END IF;
    
END //

DELIMITER ;
