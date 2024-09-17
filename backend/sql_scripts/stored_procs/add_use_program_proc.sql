USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_user_program_proc;
DELIMITER //

CREATE PROCEDURE add_user_program_proc(
	IN sub_p						VARCHAR(45),
    IN scaleModeID_p	   			INT,
    IN rhythmCollectionID_p  		INT,
    IN primaryCollectionTitle_p		VARCHAR(1000),
    IN tonicSequenceID_p 			INT,
    IN instrumentID_p				INT,
    IN scaleTonicIndex_p			INT
)

BEGIN
	DECLARE primaryCollectionID_p	INT;
    DECLARE newProgramID_p			INT;
    DECLARE newUserProgramID_p		INT;
    DECLARE message					VARCHAR(255);
    DECLARE sql_error 				BOOLEAN DEFAULT FALSE;    
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;

    START TRANSACTION;    
		SELECT collectionID 
        INTO primaryCollectionID_p
        FROM Collections
        WHERE collectionTitle = primaryCollectionTitle_p;
        
        SET message = 'A';
        
        SELECT programID 
        INTO newProgramID_p
        FROM Programs
        WHERE scaleModeID = scaleModeID_p
        AND rhythmCollectionID = rhythmCollectionID_p
        AND primaryCollectionID = primaryCollectionID_p
        AND tonicSequenceID = tonicSequenceID_p
        AND instrumentId = instrumentID_p;
	
        SET message = rhythmCollectionID_p;
        
        IF newProgramID_p IS NULL THEN
			INSERT INTO Programs (scaleModeID, rhythmCollectionID, primaryCollectionID, tonicSequenceID, instrumentID)
			VALUES (scaleModeID_p, rhythmCollectionID_p, primaryCollectionID_p, tonicSequenceID_p, instrumentID_p);
        
			SELECT LAST_INSERT_ID() INTO newProgramID_p;
            -- SET message = 'NewProgramID - Created: ';
		END IF;             
        
        SELECT userProgramID
        INTO newUserProgramID_p
        FROM UserPrograms
        WHERE programID = newProgramID_p
        AND sub = sub_p;
        
        -- SET message = 'userProgramID exists';
        
        IF newUserProgramID_p IS NULL THEN
			INSERT INTO UserPrograms (programID, currentIndex, sub, scaleTonicIndex)
			VALUES (newProgramID_p, -1, sub_p, scaleTonicIndex_p);
            SELECT LAST_INSERT_ID() INTO newUserProgramID_p;
            -- SET message = 'userProgramID created';
		END IF;
        
		IF sql_error = FALSE THEN
			-- SELECT * FROM UserPrograms 
            -- WHERE sub = sub_p;
            SELECT message AS Message;
			COMMIT;
		ELSE
			SELECT message AS message;
			ROLLBACK;
		END IF;
END //

DELIMITER ;

CALL add_user_program_proc(
	'0b44c9de-c681-479d-8f89-e8af14a57458',
    1520,
    1409,
    'melodic_minor,full_range_ascending_scale',
    273,
    537,
    1
    );

SELECT * FROM scaleModes;
SELECT collectionID
FROM Collections
WHERE collectionTitle = 'altered,one_octave_ascending_descending_scale';

SELECT * FROM UserPrograms;
DELETE FROM UserPrograms WHERE programID >= 479;
DELETE FROM Programs WHERE programID >= 479;
SELECT p.*, r.collectionTitle FROM Programs p JOIN Collections r ON p.rhythmCollectionID = r.collectionID;