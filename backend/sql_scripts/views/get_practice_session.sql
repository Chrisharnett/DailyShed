USE Daily_Shed;
CREATE OR REPLACE VIEW get_practice_session AS
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
		u.sub, 
		u.userName,        
        upr.rounds,
        ure.reviewExercise,
        up.currentIndex,
		up.userProgramID,
        up.scaleTonicIndex,
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

SELECT * FROM get_practice_session WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';

SELECT * FROM users;
    