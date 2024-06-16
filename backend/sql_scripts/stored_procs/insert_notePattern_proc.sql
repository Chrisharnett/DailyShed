USE Daily_Shed;
DROP PROCEDURE IF EXISTS insert_notePattern_proc;

DELIMITER //

CREATE PROCEDURE insert_notePattern_proc (
    IN collectionTitle_p            VARCHAR(255),
    IN collectionType_p             VARCHAR(255),
    IN collectionLength_p           INT,
    IN description_p                TEXT,
    IN directions_p                 TEXT,
    IN holdLastNote_p               BOOLEAN,
    IN notePattern_p                TEXT,
    IN notePatternType_p            VARCHAR(45),
    IN repeatMe_p                   BOOLEAN,
    IN collectionNotePatternID_p    VARCHAR(45),
    IN noteLength_p                 INT,
    IN scalePatternType_p           VARCHAR(255)
)
BEGIN 
    DECLARE collectionID_p              INT;
    DECLARE notePatternID_p             INT;
    DECLARE sql_error                   TINYINT DEFAULT FALSE;
    DECLARE message                     VARCHAR(255);
        
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            SET sql_error = TRUE;
        END;
    
    START TRANSACTION;

        -- Debug: Start transaction
        SELECT 'Start Transaction' AS debug_message;

        -- Debug: Insert into CollectionType
        SELECT 'Inserting into CollectionType', collectionType_p AS debug_message;
        INSERT IGNORE INTO CollectionType (collectionType) VALUE (collectionType_p);

        -- Debug: Selecting collectionID
        SELECT 'Selecting collectionID', collectionTitle_p, collectionType_p, collectionLength_p AS debug_message;
        SELECT collectionID INTO collectionID_p
        FROM Collections
        WHERE collectionTitle = collectionTitle_p
        AND collectionType = collectionType_p
        AND collectionLength = collectionLength_p;

        -- Debug: Check collectionID
        SELECT 'collectionID_p:', collectionID_p AS debug_message;

        IF scalePatternType_p IS NOT NULL THEN
            -- Debug: Insert into scalePatternTypes
            SELECT 'Inserting into scalePatternTypes', scalePatternType_p AS debug_message;
            INSERT IGNORE INTO scalePatternTypes (scalePatternType) VALUES (scalePatternType_p);
        END IF;

        IF collectionID_p IS NULL THEN
            -- Debug: Insert into Collections
            SELECT 'Inserting into Collections', collectionTitle_p, collectionType_p, collectionLength_p, scalePatternType_p AS debug_message;
            INSERT INTO Collections (
                collectionTitle, 
                collectionType, 
                collectionLength,
                scalePatternType
            ) VALUES (
                collectionTitle_p, 
                collectionType_p, 
                collectionLength_p,
                scalePatternType_p
            );        
            SET collectionID_p = LAST_INSERT_ID();
            -- Debug: New collectionID
            SELECT 'New collectionID:', collectionID_p AS debug_message;
        END IF;

        -- Debug: Insert into NotePatterns
        SELECT 'Inserting into NotePatterns', description_p, directions_p, holdLastNote_p, notePatternType_p, notePattern_p, repeatMe_p, collectionNotePatternID_p, noteLength_p, scalePatternType_p AS debug_message;
        INSERT INTO NotePatterns(
            description, 
            directions,
            holdLastNote,
            notePatternType, 
            notePattern,
            repeatMe,
            collectionNotePatternID,
            noteLength,
            scalePatternType
        ) VALUES (
            description_p,
            directions_p,
            holdLastNote_p,
            notePatternType_p, 
            notePattern_p,
            repeatMe_p,
            collectionNotePatternID_p,
            noteLength_p,
            scalePatternType_p
        );
        SET notePatternID_p = LAST_INSERT_ID();
        
        -- Debug: New notePatternID
        SELECT 'New notePatternID:', notePatternID_p AS debug_message;

        -- Debug: Insert into CollectionPatterns
        SELECT 'Inserting into CollectionPatterns', collectionID_p, notePatternID_p AS debug_message;
        INSERT INTO CollectionPatterns (
            CollectionID, 
            NotePatternID
        ) VALUES (
            collectionID_p,
            notePatternID_p
        );        

    IF sql_error = FALSE THEN
        COMMIT;
        SELECT 'Transaction Committed' AS debug_message;
    ELSE
        ROLLBACK;
        SELECT 'Transaction Rolled Back' AS debug_message;
    END IF;

END //

DELIMITER ;


SELECT * FROM CollectionType;
DELETE FROM CollectionType;
SELECT collectionID
FROM Collections
WHERE collectionTitle = 'major,scale_to_the_ninth'
AND collectionType = 'notePattern'
AND collectionLength = 32;

INSERT INTO Collections (
				collectionTitle, 
				collectionType, 
				collectionLength
			) VALUES (
				'major,scale_to_the_ninth', 
				'notePattern', 
				32
				);
                
INSERT IGNORE INTO scalePatternTypes (scalePatternType) VALUES ('scale_to_the_ninth');

INSERT INTO NotePatterns(
			description, 
			directions,
            holdLastNote,
            notePatternType, 
			notePattern,
            repeatMe,
			collectionNotePatternID,
            noteLength,
            scalePatternType
			) VALUES (
			'test.', 
			'["ascending", "descending", "ascending/descending", "descending/ascending"]',
			True,
            'test',
			'[2, 0]', 
            True, 
			'0',
			1, 
			'test'
			);


CALL insert_notePattern_proc('title', 
							'type', 
							333, 
							'description', 
							'["ascending", "descending", "ascending/descending", "descending/ascending"]',
							True,
							'[2, 0]', 
							'test',
							True, 
							'0',
							1, 
							'test');


USE Daily_Shed;
SELECT * FROM scalePatternTypes;
SELECT * FROM NotePatterns;
SELECT * FROM CollectionType;
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