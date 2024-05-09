USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_program_proc;
DELIMITER //

CREATE PROCEDURE add_program_proc(
    IN primaryTitle_p   VARCHAR(45),
    IN rhythmTitle_p  	VARCHAR(45),
    IN instrument_p		VARCHAR(45),
    IN scaleMode_p		VARCHAR(45),
    IN tonicSequence_p 	VARCHAR(45)
)

BEGIN
    DECLARE primaryCollectionID_p 	INT;
    DECLARE rhythmCollectionID_p 	INT;
    DECLARE scaleModeID_p 			INT;
    DECLARE instrumentID_p 			INT;
    DECLARE tonicSequenceID_p		INT;
    DECLARE message					VARCHAR(255);
    DECLARE done 					INT DEFAULT FALSE;
    DECLARE sql_error 				BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;
    
		SELECT collectionID 
        INTO primaryCollectionID_p 
        FROM Collections 
        WHERE collectionTitle = primaryTitle_p;
        
        SELECT collectionID 
        INTO rhythmCollectionID_p 
        FROM Collections 
        WHERE collectionTitle = rhythmTitle_p;
		
        SELECT instrumentID
        INTO instrumentID_p
        FROM Instruments
        WHERE instrumentName = instrument_p;
        
       --  IF tonic_p IS NULL THEN
-- 			SELECT defaultTonic 
-- 			INTO tonic_p
-- 			FROM Instruments
-- 			WHERE instrumentName = instrument_p;
-- 		END IF;
        
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
            WHERE name = 'circle of fifths';
		ELSE
			SELECT tonicSequenceID INTO tonicSequenceID_p
            FROM TonicSequences
            WHERE name = tonicSequence_p;
		END IF;
        
        INSERT INTO Programs (scaleModeID, rhythmCollectionID, primaryCollectionID, instrumentID, tonicSequenceID) 
			VALUES (scaleModeID_p, rhythmCollectionID_p, primaryCollectionID_p, instrumentID_p, tonicSequenceID_p);
            
        -- SET message = CONCAT(tonic_p, ' ', scaleModeID_p, ' ', rhythmCollectionID_p, ' ', primaryCollectionID_p, ' ', instrumentID_p, ' ', tonicSequenceID_p); 
        
		IF sql_error = FALSE THEN
		SELECT('Programs added') AS message;
        COMMIT;
		ELSE
			SELECT message AS message;
			ROLLBACK;
		END IF;
END //

DELIMITER ;

CALL add_program_proc('scale_to_the_ninth', 'quarter_note', 'saxophone', 'major', 'circle of fifths');

CALL clear_collections_and_exercises_proc;

INSERT INTO Programs (scaleModeID, rhythmCollectionID, primaryCollectionID, instrumentID, tonicSequenceID) 
			VALUES (13, 124, 123, 1, 1);
            
SELECT * FROM Programs;
SELECT * FROM TonicSequences;
SELECT * FROM Instruments;
        /*
        OPEN pitchCursor;
        pitch_loop: Loop
			FETCH pitchCursor INTO pitchName_p;
            IF done THEN
				SET done = FALSE;
				LEAVE pitch_loop;
			END IF;
            
            OPEN modeCursor;
            mode_loop: LOOP
				FETCH modeCursor INTO scaleModeID_p;
                IF done THEN
					SET done = FALSE;
					LEAVE mode_loop;
				END IF;
                */
			
			-- END LOOP mode_loop;
            -- CLOSE modeCursor;
		-- END LOOP pitch_loop;
        -- CLOSE pitchCursor;

   







