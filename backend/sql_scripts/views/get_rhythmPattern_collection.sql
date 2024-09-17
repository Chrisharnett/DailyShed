CREATE OR REPLACE VIEW get_rhythmPattern_collection AS
SELECT 
    cp.collectionID AS collectionID,
    cp.rhythmPatternID AS rhythmPatternID,
    rp.collectionRhythmPatternID AS collectionRhythmPatternID,
    rp.rhythmLength AS rhythmLength,
    rp.rhythmDescription AS rhythmDescription,
    rp.articulation AS articulation,
    rp.timeSignature AS timeSignature,
    rp.rhythmPattern AS rhythmPattern,
    rp.measures AS measureLength
FROM
    CollectionPatterns cp
    JOIN RhythmPatterns rp ON (rp.rhythmPatternID = cp.rhythmPatternID);

