USE Daily_Shed;
CREATE OR REPLACE VIEW get_user_programs AS
	 SELECT
		u.sub,
		u.userName,
        p.programID,
		pc.collectionTitle as primaryCollectionTitle,
        pc.collectionID as primaryCollectionID,
		pc.collectionLength AS collectionLength,
		pc.collectionType AS collectionType,
		i.instrumentName,
        i.abbr,
        i.level AS instrumentLevel,
		ts.name AS tonicSequenceName,
		ts.sequence,
		sm.scaleModeName,
        rc.collectionTitle AS rhythmCollectionTitle,
        rc.collectionID AS rhythmCollectionID,
		up.currentIndex,
        up.userProgramID,
        up.scaleTonicIndex
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
	
SELECT * FROM UserPrograms;
SELECT
	u.sub,
	u.userName,
-- 	p.programID,
-- 	pc.collectionTitle as primaryCollectionTitle,
-- 	pc.collectionID as primaryCollectionID,
-- 	pc.collectionLength AS collectionLength,
-- 	pc.collectionType AS collectionType,
-- 	i.instrumentName,
-- 	i.abbr,
-- 	i.level AS instrumentLevel,
-- 	ts.name AS tonicSequenceName,
-- 	ts.sequence,
-- 	sm.scaleModeName,
-- 	rc.collectionTitle AS rhythmCollectionTitle,
-- 	rc.collectionID AS rhythmCollectionID,
	up.currentIndex,
	up.userProgramID,
	up.scaleTonicIndex
FROM UserPrograms up
JOIN users u ON u.sub = up.sub
LEFT JOIN Programs p ON p.programID = up.programID
-- JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
-- JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
-- JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
-- JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
-- JOIN Instruments i ON p.instrumentID = i.instrumentID
;