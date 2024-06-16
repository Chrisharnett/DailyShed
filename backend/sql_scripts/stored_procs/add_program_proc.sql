USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_program_proc;
DELIMITER //

CREATE PROCEDURE add_program_proc(
    IN primaryTitle_p   	VARCHAR(45),
    IN rhythmTitle_p  		VARCHAR(45),
    IN scaleMode_p			VARCHAR(45),
    IN tonicSequence_p 		VARCHAR(45),
    IN instrumentName_p		VARCHAR(45),
    IN instrumentLevel_p	VARCHAR(45)
)

BEGIN
    DECLARE primaryCollectionID_p 	INT;
    DECLARE rhythmCollectionID_p 	INT;
    DECLARE scaleModeID_p 			INT;
    DECLARE tonicSequenceID_p		INT;
    DECLARE instrumentID_p			INT;
    DECLARE message					VARCHAR(255);
    DECLARE done 					INT DEFAULT FALSE;
    DECLARE sql_error 				BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;    
		
		-- SET message = CONCAT("DEBUG: ", primaryTitle_p);
        SET message = primaryTitle_p;
        
		SELECT collectionID 
        INTO primaryCollectionID_p 
        FROM Collections 
        WHERE collectionTitle = primaryTitle_p;
        
        SET message = CONCAT(primaryTitle_p, " ", primaryCollectionID_p);
        
        SELECT collectionID 
        INTO rhythmCollectionID_p 
        FROM Collections 
        WHERE collectionTitle = rhythmTitle_p;
        
        SET message = rhythmCollectionID_p;
		
        SELECT instrumentID
        INTO instrumentID_p
        FROM Instruments
        WHERE instrumentName = instrumentName_p AND
        level = instrumentLevel_p;
        
        SET message = instrumentID_p;
        
        IF scaleMode_p IS NULL THEN
			SELECT scaleModeID INTO scaleModeID_p
            FROM scaleModes
            WHERE scaleModeName = 'major';
		ELSE
			SELECT scaleModeID INTO scaleModeID_p
            FROM scaleModes
            WHERE scaleModeName = scaleMode_p;
		END IF;
        
        IF tonicSequence_p IS NULL THEN
			SELECT tonicSequenceID INTO tonicSequenceID_p
            FROM TonicSequences
            WHERE name = 'circle_of_fifths';
		ELSE
			SELECT tonicSequenceID INTO tonicSequenceID_p
            FROM TonicSequences
            WHERE name = tonicSequence_p;
		END IF;
        
        INSERT INTO Programs (scaleModeID, rhythmCollectionID, primaryCollectionID, tonicSequenceID, instrumentID) 
			VALUES (scaleModeID_p, rhythmCollectionID_p, primaryCollectionID_p, tonicSequenceID_p, instrumentID_p);
            
		SET message = CONCAT('NewProgramId: ',  LAST_INSERT_ID());
            
        -- SET message = CONCAT(tonic_p, ' ', scaleModeID_p, ' ', rhythmCollectionID_p, ' ', primaryCollectionID_p, ' ', instrumentLevel_p, ' ', instrumentID_p, ' ', tonicSequenceID_p); 
        
		IF sql_error = FALSE THEN
			SELECT('Programs added') AS message;
			COMMIT;
		ELSE
			SELECT message AS message;
			ROLLBACK;
		END IF;
END //

DELIMITER ;

CALL add_program_proc('major,scale_to_the_ninth_builder', 'quarter_note_in_4-4', 'major', 'circle_of_fifths', 'saxophone', 'beginner');

SELECT * FROM Programs;
DELETE FROM Programs;
CALL clear_collections_and_exercises_proc;

DELETE 
FROM Programs 
WHERE ProgramID = 476;

SELECT collectionID 
FROM Collections 
WHERE collectionTitle = 'quarter_note_in_4-4';
		
SELECT instrumentID
FROM Instrumentsadd_program_proc
WHERE instrumentName = 'saxophone' AND
level = 'beginner';

SELECT scaleModeID
FROM scaleModes
WHERE scaleModeName = 'major';
		
SELECT tonicSequenceID
FROM TonicSequences
WHERE name = 'circle_of_fifths';
        
INSERT INTO Programs (scaleModeID, rhythmCollectionID, primaryCollectionID, tonicSequenceID, instrumentID) 
VALUES (729, 215, 218, 96, 183);

            

SELECT * FROM TonicSequences;
SELECT * FROM Instruments;
SELECT * FROM Programs;
SELECT * FROM Collections;

   







