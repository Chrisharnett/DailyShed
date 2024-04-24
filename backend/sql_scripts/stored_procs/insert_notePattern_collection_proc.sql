USE Daily_Shed;
DROP PROCEDURE IF EXISTS insert_notePattern_collection_proc;

DELIMITER //

CREATE PROCEDURE insert_notePattern_collection_proc (
	IN collection_title_p 	VARCHAR(255),
    IN collection_type_p	VARCHAR(255),
    IN collection_length_p	INT,
    IN patterns_p			TEXT
    
)
BEGIN 
	DECLARE collectionID_p				INT;
	DECLARE finished 					TINYINT DEFAULT 0;
    DECLARE description_p				TEXT;
    DECLARE direction_p					VARCHAR(25);
    DECLARE directions_p				JSON;
    DECLARE holdLastNote_p				TINYINT DEFAULT 0;
    DECLARE notePattern_p 				JSON;
    DECLARE notePatternType_p			VARCHAR(45);
    DECLARE repeatMe_p					TINYINT DEFAULT 0;
    DECLARE collection_notePattern_ID_p INT;
    DECLARE notePatternID_p				INT;
    DECLARE i_p							INT DEFAULT 0;
    DECLARE sql_error					TINYINT DEFAULT FALSE;
    
    
    DECLARE pattern_cursor CURSOR FOR 
    SELECT 
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].notePatternType'))) AS notePatternType,
        JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].notePattern')) AS notePattern,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].description'))) AS description,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].direction'))) AS direction,
        JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].directions')) AS directions,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].repeatMe'))) AS repeatMe,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].holdLastNote'))) AS holdLastNote,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].notePatternID'))) AS collection_notePattern_ID
        FROM DUAL;
        
-- 	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
-- 		SET sql_error = TRUE;
        
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
		BEGIN
			GET DIAGNOSTICS CONDITION 1
			@sql_error_message = MESSAGE_TEXT;
			SET sql_error = TRUE;
		END;
    
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
    
    START TRANSACTION;
     
	INSERT INTO Collections (
		collection_title, 
        collection_type, 
        collection_length
	) VALUES (
        collection_title_p, 
        collection_type_p, 
        collection_length_p
        );
    SET collectionID_p = LAST_INSERT_ID();
    
    OPEN pattern_cursor;
    
	read_loop: LOOP
		FETCH pattern_cursor INTO 
			notePatternType_p, 
			notePattern_p, 
			description_p, 
			direction_p, 
			directions_p, 
			repeatMe_p, 
			holdLastNote_p, 
			collection_notePattern_ID_p;
	
		IF finished THEN
			LEAVE read_loop;
		END IF;
		
		INSERT INTO NotePatterns(
			notePatternType, 
			notePattern, 
			description, 
			direction, 
			directions, 
			repeatMe, 
			holdLastNote, 
			collection_notePattern_ID
            ) VALUES (
			notePatternType_p,
            notePattern_p,
            description_p,
            direction_p,
            directions_p,
            repeatMe_p, 
            holdLastNote_p,
			collection_notePattern_ID
			);
		SET notePatternID_p = LAST_INSERT_ID();
		
		INSERT INTO CollectionPatterns (
			CollectionID, 
			NotePatternID
		) VALUES (
			collectionID_p,
			notePatternID_p
			);
		SET i_p = i_p + 1;
        
	END LOOP;
    
    IF sql_error = FALSE THEN
		COMMIT;
        SELECT 'Transaction Comitted';
	ELSE
		ROLLBACK;
        SELECT 'Transaction failed';
	END IF;

    CLOSE pattern_cursor;

END //

DELIMITER ;


CALL insert_notePattern_collection_proc();

USE Daily_Shed;
SELECT * FROM NotePatterns;
SELECT * FROM RhythmPatterns;
SELECT * FROM Collections;
SELECT * FROM CollectionPatterns;
ALTER TABLE NotePatterns
ADD COLUMN Directions TEXT;
DELETE FROM Collections;


CALL insert_collection_proc("Test title");