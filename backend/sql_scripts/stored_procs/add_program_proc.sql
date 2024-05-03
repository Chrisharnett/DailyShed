USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_program_proc;
DELIMITER //

CREATE PROCEDURE add_program_proc(
    IN primaryTitle_p   VARCHAR(45),
    IN rhythmTitle_p  	VARCHAR(45)
)

BEGIN
    DECLARE primaryCollectionID_p INT;
    DECLARE rhythmCollectionID_p INT;
    DECLARE pitchName_p VARCHAR(8);
    DECLARE scaleModeID_p INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE sql_error BOOLEAN DEFAULT FALSE;

    DECLARE pitchCursor CURSOR FOR SELECT pitchNames FROM pitchNames;
    DECLARE modeCursor CURSOR FOR SELECT scaleModeID FROM scaleModes;    
    
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
                
                INSERT INTO Programs (tonic, scaleModeID, rhythmCollectionID, primaryCollectionID) 
				VALUES (pitchName_p, scaleModeID_p, rhythmCollectionID_p, primaryCollectionID_p);
			END LOOP mode_loop;
            CLOSE modeCursor;
		END LOOP pitch_loop;
        CLOSE pitchCursor;

    IF sql_error = FALSE THEN
		SELECT('Programs added') AS message;
        COMMIT;
    ELSE
		SELECT('ERROR, rollback') AS message, primaryCollection_p, rhythmCollection_p;
        ROLLBACK;
    END IF;
END //


DELIMITER ;


CALL add_program_proc('test', 'test');

SELECT * FROM get_practice_session;

SELECT p.tonic, sm.scaleModeName, rc.CollectionTitle AS rhythm_pattern, pc.CollectionTitle as primary_pattern
FROM Programs p 
JOIN scaleModes sm USING(scaleModeID)
LEFT JOIN Collections rc ON(p.rhythmCollectionID = rc.collectionID)
LEFT JOIN Collections pc ON(p.primaryCollectionID = pc.collectionID);


DELETE FROM Programs;
INSERT INTO Collections(collectionTitle,collectionLength, collectionType) VALUES ('test2', 876, 'test2');
INSERT INTO RhythmPatterns(rhythmDescription, articulation, timeSignature, rhythmPattern, collectionRhythmPatternID, rhythmLength)
VALUES ('test', 'test', 'test', 'test', -1, 876);
INSERT INTO NotePatterns(description, direction, directions, holdLastNote, notePattern, notePatternType, repeatMe, collectionNotePatternID, noteLength)
VALUES('test', 'test', 'test', 0, 'test', 'test', 0, -1, 876);
SELECT * FROM RhythmPatterns;
SELECT * FROM NotePatterns;
SELECT * FROM pitchNames;
SELECT * FROM scaleModes;
SELECT * FROM users;
INSERT INTO Programs (tonic, scaleModeID, rhythmCollectionID, primaryCollectionID) 
				VALUES ('a', 7, 112, 114);
CALL add_program_proc('single_note_long_tone', 'single_note_long_tone_rhythms');

SELECT * FROM Collections;

SELECT * FROM pitchNames;
