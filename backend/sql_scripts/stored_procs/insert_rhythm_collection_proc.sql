USE Daily_Shed;
DROP PROCEDURE IF EXISTS insert_rhythm_collection_proc;

DELIMITER //

CREATE PROCEDURE insert_rhythm_collection_proc (
	IN collection_title_p 	VARCHAR(255),
    IN collection_type_p	VARCHAR(255),
    IN collection_length_p	INT,
    IN patterns_p			TEXT
    
)
BEGIN 
	DECLARE collectionID_p					INT;
	DECLARE finished 						TINYINT DEFAULT 0;
    DECLARE rhythm_description_p			TEXT;
    DECLARE rhythmPatternID_p				VARCHAR(25);
    DECLARE articulation_p					JSON;
    DECLARE timeSignature_p					JSON;
    DECLARE rhythmPattern_p 				JSON;
    DECLARE collection_rhythmPattern_ID_p	INT;
    DECLARE i_p								TINYINT DEFAULT 0;
    DECLARE sql_error						TINYINT DEFAULT FALSE;
    
    DECLARE pattern_cursor CURSOR FOR SELECT 
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].rhythmDescription'))) AS rhythm_description,
        JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].rhythmPattern')) AS rhythmPattern,
        JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].articulation')) AS articulation,
        JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].timeSignature')) AS timeSignature,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', i_p, '].rhythmID'))) AS collection_rhythmPattern_ID        
        FROM DUAL;
    
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		SET sql_error = TRUE;
    
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
    
    -- OPEN pattern_cursor;
--     
-- 	read_loop: LOOP
-- 		FETCH pattern_cursor 
--         INTO  
-- 			rhythm_description_p, 
-- 			rhythmPattern_p, 
--             articulation_p, 
--             timeSignature_p, 
--             collection_rhythmPattern_ID_p;
--     
-- 		IF finished THEN
-- 			LEAVE read_loop;
--         END IF;
--         
--         INSERT INTO RhythmPatterns (
-- 				rhythm_description, 
-- 				rhythmPattern, 
-- 				articulation, 
-- 				timeSignature, 
-- 				collection_rhythmPattern_ID
--             ) VALUES (
-- 				rhythm_description_p, 
-- 				rhythmPattern_p, 
-- 				articulation_p, 
-- 				timeSignature_p, 
-- 				collection_rhythmPattern_ID_p
--             );
--         SET rhythmPatternID_p = LAST_INSERT_ID();
--     
-- 		INSERT INTO CollectionPatterns (
-- 			CollectionID, 
-- 			RhythmPatternID
-- 		) VALUES (
-- 			collectionID_p,
-- 			rhythmPatternID_p
-- 			);
-- 		SET i_p = i_p + 1;
--         
-- 	END LOOP;
    
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


USE Daily_Shed;
SELECT * FROM RhythmPatterCollectionPatternscolns;
ALTER TABLE RhythmPatterns
ADD COLUMN collection_rhythmPattern_ID INT;
DELETE FROM Collections;


CALL insert_collection_proc("Test title");