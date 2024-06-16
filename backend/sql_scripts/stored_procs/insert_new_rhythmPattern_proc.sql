USE Daily_Shed;
DROP PROCEDURE IF EXISTS insert_new_rhythmPattern_proc;

DELIMITER //

CREATE PROCEDURE insert_new_rhythmPattern_proc (
    IN collectionID_p				INT,
    IN rhythmDescription_p			TEXT,
    IN articulation_p				TEXT,
    IN timeSignature_p				TEXT,
    IN rhythmPattern_p 				TEXT,
    IN rhythmLength_p				INT,
    IN subRhythms_p					TEXT
)
BEGIN 
	DECLARE collectionRhythmPatternID_p	INT;
    DECLARE rhythmPatternID_p				INT;
    DECLARE sql_error						TINYINT DEFAULT FALSE;
        
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		BEGIN
			SET sql_error = TRUE;
		END;
    
    START TRANSACTION;
    
    -- add validation the rhythmPattern doesn't already exist
		SELECT rhythmPatternID INTO rhythmPatternID_p 
        FROM RhythmPatterns
        WHERE rhythmDescription = rhythmDescription_p AND
			articulation = articulation_p AND
			timeSignature = timeSignature_p AND
			rhythmPattern = rhythmPattern_p AND
            rhythmLength = rhythmLength_p;
		
        IF rhythmPatternID_p IS NULL THEN    
			SELECT MAX(collectionRhythmPatternID) + 1 
			INTO collectionRhythmPatternID_p 
			FROM RhythmPatterns;
			
			INSERT INTO RhythmPatterns(
				rhythmDescription,
				articulation,
				timeSignature,
				rhythmPattern,
				collectionRhythmPatternID,
				rhythmLength,
                subRhythms
				) VALUES (
				rhythmDescription_p,
				articulation_p,
				timeSignature_p,
				rhythmPattern_p,
				collectionRhythmPatternID_p,
				rhythmLength_p,
                subRhythms
				);
			SET rhythmPatternID_p = LAST_INSERT_ID();
				
			INSERT INTO CollectionPatterns (
				collectionID, 
				rhythmPatternID
			) VALUES (
				collectionID_p,
				rhythmPatternID_p
				);
		END IF;

    IF sql_error = FALSE THEN
		COMMIT;
        SELECT rhythmPatternID_p AS rhythmPatternID;
	ELSE
		ROLLBACK;
        SELECT 'Transaction failed';
	END IF;

END //

DELIMITER ;

USE Daily_Shed;
SELECT * FROM NotePatterns;
SELECT * FROM RhythmPatterns;
SELECT * FROM CollectionPatterns;

SELECT exerciseID FROM Exercises WHERE rhythmPatternID = 467;
DELETE FROM UserPracticeSessionExercises WHERE exerciseID = 174;
DELETE FROM ProgramExercises WHERE exerciseID = 174;
DELETE FROM ExerciseLog WHERE exerciseID = 174;
DELETE FROM Exercises WHERE exerciseID = 174;
DELETE FROM CollectionPatterns WHERE rhythmPatternID = 467;
DELETE FROM RhythmPatterns WHERE rhythmPatternID = 467;

DELETE FROM Exercises WHERE rhythmPatternID = 465;
DELETE FROM RhythmPatterns 
WHERE rhythmPatternID = 465;

SELECT * FROM Collections;
SELECT * FROM CollectionPatterns;

ALTER TABLE Collections
ADD CONSTRAINT unique_collection UNIQUE (collectionTitle);

DELETE FROM CollectionPatterns;
DELETE FROM NotePatterns;
DELETE FROM RhythmPatterns;
DELETE FROM Collections;



ALTER TABLE NotePatterns
ADD COLUMN Directions TEXT;
DELETE FROM Collections;
DROP PROCEDURE IF EXISTS insert_rhythm_collection_proc;


CALL insert_collection_proc("Test title");