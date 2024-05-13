USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_new_exercise_proc;
DELIMITER //

CREATE PROCEDURE add_new_exercise_proc(
    IN notePatternID_p   		INT,
    IN rhythmPatternID_p		INT,
    IN tonic_p					VARCHAR(25),
    IN mode_p					VARCHAR(45),
    IN direction_p				VARCHAR(45),
    IN directionIndex_p			INT,
    IN userProgramID_p			INT,
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
		SELECT description INTO description_p
        FROM NotePatterns
        WHERE notePatternID = notePatternID_p;
        
        SELECT REPLACE(CONCAT(UPPER(LEFT(c.collectionTitle, 1)), LOWER(SUBSTRING(c.collectionTitle, 2))), '_', ' ')
        INTO collectionTitle_p
        FROM Collections c
        JOIN CollectionPatterns cp 
        ON cp.collectionID = c.collectionID
        WHERE cp.notePatternID = notePatternID_p;
        
        SELECT REPLACE(REPLACE(REPLACE(REPLACE(timeSignature, '[', ''), ']', ''), ',', '/'), ' ', '')
        INTO timeSignature_p
        FROM RhythmPatterns
        WHERE rhythmPatternID = rhythmPatternID_p;
        
        SELECT exerciseID INTO exerciseID_p
		FROM Exercises
		WHERE notePatternID = notePatternID_p
		  AND rhythmPatternID = rhythmPatternID_p
		  AND tonic = tonic_p
		  AND mode = mode_p
		  AND directionIndex = directionIndex_p;
		
        
        IF exerciseID_p IS NULL THEN
			SELECT CONCAT(
			COALESCE(CONCAT(UPPER(LEFT(tonic_p, 1)), LOWER(SUBSTRING(tonic_p, 2))), ''), ' ',
			COALESCE(CONCAT(UPPER(LEFT(mode_p, 1)), LOWER(SUBSTRING(mode_p, 2))), ''), ' ',
			COALESCE(collectionTitle_p, ''), ' in ',
			COALESCE(timeSignature_p, ''), ' '
			)
			INTO exerciseName_p;
			
			 IF direction_p <> 'static' THEN
				SET exerciseName_p =  CONCAT(exerciseName_p, ' ',UPPER(LEFT(direction_p, 1)), LOWER(SUBSTRING(direction_p, 2)));
			END IF;
			
			SELECT RTRIM(exerciseName_p) INTO exerciseName_p;        
			
			
			
			INSERT INTO Exercises(
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
		END IF;
        
        SELECT programID INTO programID_p
        FROM UserPrograms 
        WHERE userProgramID = userProgramID_p;
        
        INSERT INTO ProgramExercises (ExerciseID, programID) VALUES (exerciseID_p, programID_p);
        
        INSERT INTO UserPracticeSessionExercises (exerciseID, UserPracticeSessionID) VALUES (exerciseID_p, userPracticeSessionID_p);
        
		-- SELECT CONCAT(exerciseID_p, '-', REPLACE(exerciseName_p, ' ', '_')) INTO imageFilename_p;
        SELECT CONCAT(exerciseID_p) INTO imageFilename_p;
        
        UPDATE Exercises
        SET imageFilename = imageFilename_p
        WHERE ExerciseID = exerciseID_p;  
        
SELECT 
	exerciseID_p AS exerciseID,
	imageFilename_p AS imageFilename,
	exerciseName_p AS exerciseName,
	description_p AS description;
    
    IF sql_error_code = 0 THEN
		COMMIT;
	ELSE
		ROLLBACK; -- This is redundant due to the handler but can be explicitly stated for clarity
		SELECT 'Transaction rolled back due to error:', sql_error_message AS Error_Message;
	END IF;
    
END //

DELIMITER ;


CALL add_new_exercise_proc(524, 392, 'c', 'major', 'static', 0, 130, 136);
SELECT * FROM Exercises;
SELECT * FROM RhythmPatterns;
SELECT * FROM NotePatterns;
SELECT * FROM UserPrograms;
SELECT * FROM UserPracticeSession;

CALL clear_exercises_proc();
-- SELECT * FROM view_exercises;

-- SELECT * FROM NotePatterns;
DELETE FROM UserPracticeSessionExercises;
DELETE FROM ProgramExercises;
DELETE FROM Exercises;