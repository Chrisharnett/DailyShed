USE Daily_Shed;
CREATE OR REPLACE VIEW get_routine AS
	SELECT 
		u.sub, 
		u.userName,        
        upr.rounds,
        ure.reviewExercise,
        up.currentIndex,
		up.userProgramID,
        up.scaleTonicIndex,
        p.programID,
        p.rhythmCollectionID,
		p.primaryCollectionID,
		p.scaleModeID,
        ts.sequence AS tonicSequence,
		sm.scaleModeName AS mode,
		pc.collectionLength AS collectionLength,
		pc.collectionType AS PrimaryCollectionType,
		pc.scalePatternType,
		pc.collectionTitle AS PrimaryCollectionTitle,
		rc.collectionTitle AS rhythmCollectionTitle,
		i.instrumentName,
		i.lowNote,
		i.highNote,
		i.level,
		i.defaultTonic,
		i.abbr
    FROM users u 
    JOIN UserPracticeRoutines upr ON(upr.sub = u.sub)
    JOIN UserRoutineExercises ure ON(ure.UserPracticeRoutineID = upr.UserPracticeRoutineID)
    JOIN UserPrograms up ON up.userProgramID = ure.userProgramID
	JOIN Programs p ON(p.programID = up.programID)
	JOIN Instruments i ON i.instrumentID = p.instrumentID	
    JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
	JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
	LEFT JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
	LEFT JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
	WHERE upr.isActive = true
    ;
  
  SELECT 
	p.programID, 
	sm.scaleModeName, 
    rc.collectionTitle AS rhythmCollection, 
    pc.collectionTitle AS primaryCollection,
    ts.name AS tonicSequence,
    c.category
FROM Programs p JOIN scaleModes sm ON p.scaleModeID = sm.scaleModeID
JOIN Collections rc ON p.rhythmCollectionID = rc.collectionID
JOIN Collections pc ON p.primaryCollectionID = pc.collectionID
JOIN TonicSequences ts ON p.tonicSequenceID = ts.tonicSequenceID
JOIN ProgramCategories c ON p.category = c.programCategoryID;
    