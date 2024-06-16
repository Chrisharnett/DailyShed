USE Daily_Shed;
CREATE OR REPLACE VIEW get_user_programs AS
	 SELECT
		u.userName,
		pc.collectionTitle,
		pc.collectionLength,
		pc.collectionType,
		i.instrumentName,
        i.level AS instrumentLevel,
		ts.name AS tonicSequenceName,
		ts.sequence,
		sm.scaleModeName,
        rc.collectionTitle AS rhythmCollection,
		up.* 
	FROM UserPrograms up
    JOIN users u ON u.sub = up.sub
	LEFT JOIN Programs p ON p.programID = up.programID
    JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
	JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
	JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
	JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
	JOIN Instruments i ON p.instrumentID = i.instrumentID
	;

   SELECT * FROM get_user_programs WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
	
    SELECT
		u.userName,
		pc.collectionTitle,
		pc.collectionLength,
		pc.collectionType,
		i.instrumentName,
		ts.name AS tonicSequenceName,
		ts.sequence,
		sm.scaleModeName,
        rc.collectionTitle AS rhythmCollection,
		up.* 
	FROM UserPrograms up
    JOIN users u ON u.sub = up.sub
	LEFT JOIN Programs p ON p.programID = up.programID
    JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
	JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
	JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
	JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
	JOIN Instruments i ON p.instrumentID = p.instrumentID
	WHERE u.sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
    
    SELECT * FROM RhythmPatterns;
    