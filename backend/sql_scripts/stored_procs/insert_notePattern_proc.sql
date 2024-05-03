USE Daily_Shed;
DROP PROCEDURE IF EXISTS insert_notePattern_proc;

DELIMITER //

CREATE PROCEDURE insert_notePattern_proc (
	IN collectionTitle_p 			VARCHAR(255),
    IN collectionType_p				VARCHAR(255),
    IN collectionLength_p			INT,
    IN description_p				TEXT,
    IN direction_p					VARCHAR(45),
    IN directions_p					TEXT,
    IN holdLastNote_p				BOOLEAN,
    IN notePattern_p				TEXT,
    IN notePatternType_p			VARCHAR(45),
    IN repeatMe_p					BOOLEAN,
    IN collectionNotePatternID_p	VARCHAR(45),
    IN noteLength_p					INT
)
BEGIN 
	DECLARE collectionID_p				INT;
    DECLARE notePatternID_p				INT;
    DECLARE sql_error					TINYINT DEFAULT FALSE;
        
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		BEGIN
			SET sql_error = TRUE;
		END;
    
    START TRANSACTION;
        SELECT collectionID INTO collectionID_p
        FROM Collections
        WHERE collectionTitle = collectionTitle_p
			AND collectionType = collectionType_p
            AND collectionLength = collectionLength_p;
		
        If collectionID_p IS NULL THEN
			INSERT IGNORE INTO Collections (
				collectionTitle, 
				collectionType, 
				collectionLength
			) VALUES (
				collectionTitle_p, 
				collectionType_p, 
				collectionLength_p
				);
		
			SET collectionID_p = LAST_INSERT_ID();
		END IF;
    
		INSERT INTO NotePatterns(
			description, 
			direction, 
			directions,
            holdLastNote,
            notePatternType, 
			notePattern,
            repeatMe,
			collectionNotePatternID,
            noteLength
			) VALUES (
			description_p, 
			direction_p, 
			directions_p,
            holdLastNote_p,
            notePatternType_p, 
			notePattern_p,
            repeatMe_p,
			collectionNotePatternID_p,
            noteLength_p
			);
		SET notePatternID_p = LAST_INSERT_ID();
			
		INSERT INTO CollectionPatterns (
			CollectionID, 
			NotePatternID
		) VALUES (
			collectionID_p,
			notePatternID_p
			);        

    IF sql_error = FALSE THEN
		COMMIT;
        SELECT 'Transaction Comitted';
	ELSE
		ROLLBACK;
        SELECT 'Transaction failed';
	END IF;

END //

DELIMITER ;


CALL insert_notePattern_proc(
    "Test 3 Collection",
    "notePattern 3",
    2,
    "Description for new pattern",
    "test direction 2",
    "[test directions 2]",
    FALSE,
    "[1,2, 3]",
    "test notepatternType 3",
    FALSE,
    "test notepattern ID 2"    
);

INSERT INTO Collections (
			collectionTitle, 
			collectionType, 
			collectionLength
		) VALUES (
			"asdf", 
			"test", 
			5
			);

INSERT INTO NotePatterns(
			notePatternType, 
			notePattern, 
			description, 
			direction, 
			directions, 
			repeatMe, 
			holdLastNote, 
			collectionNotePatternID
			) VALUES (
			"TYPE",
			"[1,2]",
			"DESCRIPTION",
			"test",
			"[test]",
			TRUE, 
			FALSE,
			22
			);
INSERT INTO CollectionPatterns (collectionID, notePatternID) VALUES (1, 1);

USE Daily_Shed;
SELECT * FROM NotePatterns;
SELECT * FROM RhythmPatterns;
SELECT * FROM Collections;
SELECT * FROM CollectionPatterns;

ALTER TABLE Collections
ADD CONSTRAINT unique_collection UNIQUE (collectionTitle);

DELETE FROM CollectionPatterns;
DELETE FROM NotePatterns;
DELETE FROM Collections;



ALTER TABLE NotePatterns
ADD COLUMN Directions TEXT;
DELETE FROM Collections;
DROP PROCEDURE IF EXISTS insert_rhythm_collection_proc;


CALL insert_collection_proc("Test title");