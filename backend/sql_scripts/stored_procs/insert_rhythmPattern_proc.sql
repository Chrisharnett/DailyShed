USE Daily_Shed;
DROP PROCEDURE IF EXISTS insert_rhythmPattern_proc;

DELIMITER //

CREATE PROCEDURE insert_rhythmPattern_proc (
	IN collectionTitle_p 				VARCHAR(255),
    IN collectionType_p					VARCHAR(255),
    IN collectionLength_p				INT,
    IN rhythmDescription_p				TEXT,
    IN articulation_p					TEXT,
    IN timeSignature_p					TEXT,
    IN rhythmPattern_p 					TEXT,
    IN collectionRhythmPatternID_p		INT,
    IN rhythmLength_p					INT
)
BEGIN 
	DECLARE collectionID_p				INT;
    DECLARE rhythmPatternID_p			INT;
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
		
        IF collectionID_p IS NULL THEN
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
        
		INSERT INTO RhythmPatterns(
			rhythmDescription,
			articulation,
			timeSignature,
			rhythmPattern,
			collectionRhythmPatternID,
            rhythmLength
			) VALUES (
			rhythmDescription_p,
			articulation_p,
			timeSignature_p,
			rhythmPattern_p,
			collectionRhythmPatternID_p,
            rhythmLength_p
			);
		SET rhythmPatternID_p = LAST_INSERT_ID();
			
		INSERT INTO CollectionPatterns (
			collectionID, 
			rhythmPatternID
		) VALUES (
			collectionID_p,
			rhythmPatternID_p
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


CALL insert_rhythmPattern_proc(
    "Test 3 rhy Collection",
    "rhythm Pattern rhy 3",
    2,
    "description",
	23,
	"sdfgsdfg",
	"sdfgsdfg",
	"sdfgsdfg"    
);


USE Daily_Shed;
SELECT * FROM NotePatterns;
SELECT * FROM RhythmPatterns;
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