def MatchHashes(
    queryHashes,
    database
):

    offsetCounts = {}

    for hashValue, queryTime in queryHashes:

        if hashValue not in database:
            continue

        matches = database[hashValue]

        for songName, dbTime in matches:

            deltaOffset = (
                dbTime
                -
                queryTime
            )

            key = (
                songName,
                deltaOffset
            )

            if key not in offsetCounts:
                offsetCounts[key] = 0

            offsetCounts[key] += 1

    return offsetCounts

def BestMatch(offsetCounts):

    bestSong = None
    bestCount = 0

    for key, count in offsetCounts.items():

        songName, offset = key

        if count > bestCount:

            bestCount = count
            bestSong = songName

    return bestSong, bestCount
