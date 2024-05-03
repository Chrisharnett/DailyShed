def chooseDirection(directionsPlayed):
    directions = [
        "ascending",
        "descending",
        "ascending descending",
        "descending ascending",
    ]
    newDirections = [direction for direction in directions if direction not in directionsPlayed]
    if 0 < len(newDirections):
        return newDirections[0]
    return directions[random.randint(0, len(directions) - 1)]

def descendingPattern(pattern):
    d = pattern.get('notePattern').copy()
    d.reverse()
    pattern['notePattern'] = d
    pattern['direction'] = 'descending'
    return pattern

def ascendingDescendingPattern(pattern):
    a = pattern.get('notePattern').copy()
    d = pattern.get('notePattern').copy()
    d.reverse()
    a.pop()
    a.extend(d)
    pattern['notePattern'] = a
    pattern['direction'] = 'ascending descending'
    return pattern

def descendingAscendingPattern(pattern):
    d = pattern.get('notePattern').copy()
    d.reverse()
    d.pop()
    d.extend(pattern.get("notePattern"))
    pattern['notePattern'] = d
    pattern['direction'] = 'descending ascending'
    return pattern