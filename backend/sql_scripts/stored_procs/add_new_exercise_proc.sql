USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_new_exercise_proc;
DELIMITER //

CREATE PROCEDURE add_new_exercise_proc(
    IN notePatternID_p   		INT,
    IN rhythmPatternID_p		INT,
    IN tonic_p					INT,
    IN mode_p					INT,
    IN direction_p				VARCHAR(25),
    IN directionIndex_p			INT,
    IN userProgramID_p				INT,
    IN userPracticeSessionID_p	INT
)

BEGIN
    DECLARE exerciseID_p 		INT 			DEFAULT NULL;
    DECLARE exerciseName_p		VARCHAR(45) 	DEFAULT NULL;
    DECLARE imageFilename_p		VARCHAR(45) 	DEFAULT NULL;
    DECLARE description_p		VARCHAR(255)	DEFAULT NULL;
    DECLARE imageURL_p			VARCHAR(45)		DEFAULT NULL;
    DECLARE patternType_p		VARCHAR(45)		DEFAULT NULL;
    DECLARE collectionTitle_p	VARCHAR(255)	DEFAULT NULL;
    DECLARE programTitle_p		VARCHAR(255)	DEFAULT NULL;
    DECLARE timeSignature_p		VARCHAR(45)		DEFAULT NULL;
    DECLARE programID_p			INT				DEFAULT NULL;
    
    DECLARE sql_error BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;

    START TRANSACTION;
		SELECT description INTO description_p
        FROM NotePatterns
        WHERE notePatternID = notePatternID_p;
        
        SELECT REPLACE(CONCAT(UPPER(LEFT(c.collectionTitle, 1)), LOWER(SUBSTRING(c.collectionTitle, 2))), '_', ' ')
        INTO collectionTitle_p
        FROM Collections c
        JOIN CollectionPatterns cp 
        ON cp.collectionID = c.collectionID
        WHERE cp.notePatternID = notePatternID_p;
        
        SELECT REPLACE(REPLACE(REPLACE(timeSignature, '[', ''), ']', ''), ',', ' /')
        INTO timeSignature_p
        FROM RhythmPatterns
        WHERE rhythmPatternID = rhythmPatternID_p;
        
		SELECT 
			CONCAT(
				CONCAT(UPPER(LEFT(tonic_p, 1)), LOWER(SUBSTRING(tonic_p, 2))), ' ',
                CONCAT(UPPER(LEFT(mode_p, 1)), LOWER(SUBSTRING(mode_p, 2))), ' ',
                collectionTitle_p, ' ', 'in ',
                timeSignature_p, ' ',
                CONCAT(UPPER(LEFT(direction_p, 1)), LOWER(SUBSTRING(direction_p, 2))), '.'
            ) 
		INTO exerciseName_p;
        
        
        INSERT IGNORE INTO Exercises(
			notePatternID, 
            rhythmPatternID,
            exerciseName,
            tonic,
            mode,
            description,
            directionIndex
            ) VALUES (
            notePatternID_p,
            rhythmPatternID_p,
            exerciseName_p,
            tonic_p,
            mode_p,
            description_p,
            directionIndex_p
            );
            
		SELECT LAST_INSERT_ID() INTO exerciseID_p;
        
        SELECT programID INTO programID_p
        FROM UserPrograms 
        WHERE userProgramID = userProgramID_p;
        
        INSERT INTO ProgramExercises (ExerciseID, programID) VALUES (exerciseID_p, programID_p);
        
        INSERT INTO UserPracticeSessionExercises (exerciseID, UserPracticeSessionID) VALUES (exerciseID_p, userPracticeSessionID_p);
        
		SELECT CONCAT(programID_p, '-', exerciseID_p) INTO imageFilename_p;
        
        UPDATE Exercises
        SET imageFilename = imageFilename_p
        WHERE ExerciseID = exerciseID_p;  
        
SELECT 
	exerciseID_p AS exerciseID,
	imageFilename_p AS imageFilename,
	exerciseName_p AS exerciseName,
	description_p AS description;
    
    IF sql_error = FALSE THEN
        COMMIT;
    ELSE
		SELECT('ERROR, rollback') AS message;
        ROLLBACK;
    END IF;
    
END //

DELIMITER ;

SELECT * FROM UserPrograms;


SELECT REPLACE(CONCAT(UPPER(LEFT(description, 1)), LOWER(SUBSTRING(description, 2))), '_', ' ') AS description_p
        FROM NotePatterns
        ;
        
SELECT REPLACE(CONCAT(UPPER(LEFT(c.collectionTitle, 1)), LOWER(SUBSTRING(c.collectionTitle, 2))), '_', ' ')
-- INTO collectionTitle_p
FROM Collections c
JOIN CollectionPatterns cp 
ON cp.collectionID = c.collectionID
-- WHERE cp.notePatternID = notePatternID_p
;

SELECT REPLACE(REPLACE(timeSignature, '[', ''), ']', '') AS CleanBrackets
	-- REPLACE(REPLACE(REPLACE(timeSignature, '[', ''), ']', ''), ',', ' /') AS TimeSignature
FROM RhythmPatterns;
