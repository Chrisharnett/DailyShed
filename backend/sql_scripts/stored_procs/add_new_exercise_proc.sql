USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_new_exercise_proc;
DELIMITER //

CREATE PROCEDURE add_new_exercise_proc(
    IN notePatternID_p   	INT,
    IN rhythmPatternID_p	INT,
    IN tonic_p				INT,
    IN mode_p				INT,
    IN directionIndex_p		INT,
    IN programID_p			INT
)

BEGIN
    DECLARE exerciseID_p 		INT 			DEFAULT NULL;
    DECLARE exerciseName_p		VARCHAR(45) 	DEFAULT NULL;
    DECLARE imageURL_p			VARCHAR(45) 	DEFAULT NULL;
    DECLARE description_p		VARCHAR(255)	DEFAULT NULL;
    
    DECLARE sql_error BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;

    START TRANSACTION;
		INSERT IGNORE INTO Exercises(
			notePatternID, 
            rhythmPatternID,
            exerciseName,
            tonic,
            mode,
            imageURL,
            description,
            directionIndex
            ) VALUES (
            notePatternID_p,
            rhythmPatternID_p,
            exerciseName_p,
            tonic_p,
            mode_p,
            imageURL_p,
            description_p,
            directionIndex_p
            );
            
		SELECT LAST_INSERT_ID INTO exerciseID_p;
        -- INSERT INTO USER PRACTICE SESSION    

    
    
    IF sql_error = FALSE THEN
		SELECT exerciseID_p AS ExerciseID;
        COMMIT;
    ELSE
		SELECT('ERROR, rollback') AS message, primaryCollection_p, rhythmCollection_p;
        ROLLBACK;
    END IF;
    
END //

DELIMITER ;
