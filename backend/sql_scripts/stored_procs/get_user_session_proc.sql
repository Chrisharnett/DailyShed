USE Daily_Shed;
DROP PROCEDURE IF EXISTS get_user_session_proc;
DELIMITER //

CREATE PROCEDURE get_user_session_proc(
    IN sub_p   			VARCHAR(45)
)

BEGIN
    DECLARE primaryCollectionID_p 	INT;
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

SELECT g.tonic, 
	g.scaleModeID, 
	g.rounds, 
	g.setLength, 
	g.reviewExercise, 
	g.currentIndex, 
	g.collectionLength, 
	g.rhythmCollectionID, 
	g.primaryCollectionID,
    g.userProgramID,
	np.notePatternID AS sessionNotePattern
FROM get_practice_session g
JOIN CollectionPatterns c ON c.collectionID = g.primaryCollectionID
JOIN NotePatterns np ON np.notePatternID = c.notePatternID
WHERE g.userName = 'Chris Harnett'
AND np.collectionNotePatternID = (currentIndex + 1);

SELECT * FROM get_practice_session;
