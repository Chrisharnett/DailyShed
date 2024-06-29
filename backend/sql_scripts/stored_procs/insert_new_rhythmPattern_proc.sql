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
    IN subRhythms_p					TEXT,
    IN measureLength_p				INT
)
BEGIN 
	DECLARE collectionRhythmPatternID_p		INT;
    DECLARE rhythmPatternID_p				INT;
    DECLARE message							VARCHAR(45);
    DECLARE sql_error						TINYINT DEFAULT FALSE;
        
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		BEGIN
			SET sql_error = TRUE;
		END;
    
    START TRANSACTION;
    
		SELECT rhythmPatternID INTO rhythmPatternID_p 
        FROM RhythmPatterns
        WHERE rhythmDescription = rhythmDescription_p AND
			articulation = articulation_p AND
			timeSignature = timeSignature_p AND
			rhythmPattern = rhythmPattern_p AND
            rhythmLength = rhythmLength_p AND
            measures = measureLength_p AND
            subRhythms = subRhythms_p
		LIMIT 1;
		
			SET message = 'first RP ID';
            
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
                subRhythms,
                measures
				) VALUES (
				rhythmDescription_p,
				articulation_p,
				timeSignature_p,
				rhythmPattern_p,
				collectionRhythmPatternID_p,
				rhythmLength_p,
                subRhythms_p,
                measureLength_p
				);
			SET rhythmPatternID_p = LAST_INSERT_ID();
            
            SET message = 'rhythmPatternID';
				
			INSERT INTO CollectionPatterns (
				collectionID, 
				rhythmPatternID
			) VALUES (
				collectionID_p,
				rhythmPatternID_p
				);
                
			SET message = CONCAT(rhythmPatternID_p, '-', LAST_INSERT_ID());
            
		END IF;

    IF sql_error = FALSE THEN
		COMMIT;
        SELECT rhythmPatternID_p AS rhythmPatternID;
	ELSE
		ROLLBACK;
        SELECT message as ErrorMessage;
	END IF;

END //

DELIMITER ;

CALL insert_new_rhythmPattern_proc(
	1409, 
	'multi-measure pattern', 
	'[]', 
	'[4, 4]', 
	'[["4"], ["4"], ["4"], ["4"], [4], ["r4"], [4], [4]]', 
	7,
	'[2621, 2633]',
	2)
    ;
    
SELECT rhythmPatternID
FROM RhythmPatterns
WHERE rhythmDescription = 'multi-measure pattern' 
AND articulation = '[]' 
AND timeSignature = '[4, 4]' 
AND rhythmPattern = '[["4"], ["4"], ["4"], ["4"], [4], ["r4"], [4], [4]]'
AND rhythmLength = 7 
AND measureLength = 2 
AND subRhythms = '[2621, 2633]'
;