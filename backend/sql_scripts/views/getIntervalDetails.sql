USE Daily_Shed;
DROP PROCEDURE IF EXISTS get_interval_details_proc
DELIMITER //

CREATE PROCEDURE get_interval_details_proc(
    IN notePatternID_p   			INT,
    IN rhythmPatternID_p			INT,
    IN sub_p						VARCHAR(45)
		
)

BEGIN
    DECLARE directionIndex_p 		INT;
    DECLARE rhythmCollectionID_p 	INT;
    
    DECLARE done INT DEFAULT FALSE;
    DECLARE sql_error BOOLEAN DEFAULT FALSE;

    DECLARE intervalCursor CURSOR FOR 
    SELECT primaryCollectionID, rhythmCollectionID_p
    FROM get_session_patterns WHERE sub = sub_p;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;
    -- will return correct notePatternCollections, rhythmPatternCollection + interval info.
		OPEN intervalCursor;
        interval_loop: LOOP
			FETCH intervalCursor
            INTO primaryCollectionID_p, rhythmCollectionID_p;
            IF done THEN
				LEAVE interval_loop;
			END IF;
			
            SELECT collectionID, notePatternID
            FROM CollectionPatterns cp
            WHERE primaryCollectionID_p = cp.collectionID;
            
            SELECT collectionID, rhythmPatternID
            FROM CollectionPatterns cp
            WHERE rhythmCollectionID_p = cp.collectionID;
		
        END LOOP interval_loop;
        CLOSE intervalCursor;
        
        SELECT * FROM get_session_details WHERE sub = sub_p;     
	
    IF sql_error = FALSE THEN
		SELECT('Programs added') AS message;
        COMMIT;
    ELSE
		SELECT('ERROR, rollback') AS message, primaryCollection_p, rhythmCollection_p;
        ROLLBACK;
    END IF;
    
END //

DELIMITER ;