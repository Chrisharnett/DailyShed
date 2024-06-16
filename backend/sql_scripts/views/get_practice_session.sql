USE Daily_Shed;
CREATE OR REPLACE VIEW get_practice_session AS
	SELECT 
		u.sub, 
		u.userName,
        pc.collectionTitle AS PrimaryCollectionTitle,
        rc.collectionTitle AS rhythmCollectionTitle,
        p.scaleModeID,
        sm.scaleModeName AS mode,
        ts.sequence AS tonicSequence,
        up.scaleTonicIndex,
        upr.rounds,
        upr.setLength,
        ure.reviewExercise,
        up.currentIndex,
        up.userProgramID,
		pc.collectionLength AS collectionLength,
		pc.collectionType AS PrimaryCollectionType,
        pc.scalePatternType,
        p.rhythmCollectionID,
        p.primaryCollectionID,
        i.instrumentName,
        i.lowNote,
        i.highNote,
        i.level,
        i.defaultTonic
    FROM users u 
    JOIN UserPrograms up ON u.sub = up.sub
    JOIN UserRoutineExercises ure ON(ure.UserProgramID = up.UserProgramID)
    JOIN UserPracticeRoutines upr ON(upr.sub = u.sub)
    JOIN Programs p ON(p.programID = up.programID)
    JOIN Instruments i ON i.instrumentID = p.instrumentID
	JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
    JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
    LEFT JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
    LEFT JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
    ;

SELECT 
		u.sub, 
		u.userName,
        -- pc.collectionTitle AS PrimaryCollectionTitle,
--         rc.collectionTitle AS rhythmCollectionTitle,
--         p.scaleModeID,
--         sm.scaleModeName AS mode,
--         ts.sequence AS tonicSequence,
        up.scaleTonicIndex,
        up.currentIndex,
        up.userProgramID,
        -- upr.rounds,
        -- upr.setLength,
		ure.reviewExercise        
		-- pc.collectionLength AS collectionLength,
-- 		pc.collectionType AS PrimaryCollectionType,
--         pc.scalePatternType,
--         p.rhythmCollectionID,
--         p.primaryCollectionID,
--         i.instrumentName,
--         i.lowNote,
--         i.highNote,
--         i.level,
--         i.defaultTonic
    FROM users u 
    JOIN UserPrograms up ON u.sub = up.sub
    JOIN UserRoutineExercises ure ON(ure.UserProgramID = up.UserProgramID)
    -- JOIN UserPracticeRoutines upr ON(upr.sub = u.sub)
--     JOIN Programs p ON(p.programID = up.programID)
--     JOIN Instruments i ON i.instrumentID = p.instrumentID
-- 	JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
--     JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
--     LEFT JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
--     LEFT JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
    WHERE u.userName = 'Chris Harnett';
    
SELECT * FROM users;
SELECT * FROM UserPrograms;
SELECT * FROM Programs;
SELECT * FROM RhythmPatterns;
SELECT * FROM Instruments;
SELECT * FROM UserPracticeRoutines;
DELETE FROM UserPracticeRoutines WHERE UserPracticeRoutineID = 87;
SELECT * FROM get_practice_session;

ALTER TABLE Daily_Shed.RhythmPatterns 
ADD COLUMN measures INT NULL DEFAULT 1 AFTER rhythmLength;
    