USE Daily_Shed;
DROP PROCEDURE IF EXISTS get_next_pitch_pattern_proc;
DELIMITER //

CREATE PROCEDURE get_next_pitch_pattern_proc(
    IN sub_p   			VARCHAR(45)
)

BEGIN
    DECLARE primaryCollectionID_p 	INT;
    DECLARE notePatternID_p 		INT;
    DECLARE reviewExercise_p 		BOOLEAN;
    DECLARE newIndex_p				INT;
    DECLARE userProgramID_p			INT;
    DECLARE setLength_p				INT;
    
    DECLARE done INT DEFAULT FALSE;
    DECLARE sql_error BOOLEAN DEFAULT FALSE;

    DECLARE intervalCursor CURSOR FOR 
    SELECT primaryCollectionID, reviewExercise, currentIndex, userProgramID , setLength
    FROM get_session_patterns WHERE sub = sub_p;

    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;
		OPEN intervalCursor;
        interval_loop: LOOP
			FETCH intervalCursor
            INTO primaryCollectionID_p, reviewExercise_p, currentIndex_p, userProgramID_p, setLength_p;
			
            If reviewExercise_p IS FALSE OR currentIndex_p = -1 THEN
				-- increment currentIndex
				UPDATE UserPrograms 
                SET currentIndex = (currentIndex + 1) % setLength_p
                WHERE sub = sub_p AND userProgramID = userProgramID_p;
                -- update currentIndex_p
                SELECT currentIndex INTO currentIndex_p
                FROM UserPrograms up JOIN users u ON up.sub = u.sub
                WHERE u.sub = sub_p AND  up.userProgramID = userProgramID_p;
                
                SELECT np.notePatternID INTO notePatternID_p
				FROM NotePatterns np
                JOIN CollectionPatterns cp ON cp.notePatternID = np.notePatternID
                JOIN Programs p ON cp.collectionID = p.primaryCollectionID
                JOIN UserPrograms up ON p.programID = up.programID
                WHERE currentIndex = currentIndex_p;				
			-- ADD review patterns Logic, May have to do that in Python.
            END IF;
       
		END LOOP interval_loop;
        CLOSE intervalCursor;
	
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
