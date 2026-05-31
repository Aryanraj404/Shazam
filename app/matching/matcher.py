import psycopg2

from app.audio.fingerprint import GenerateConstellationMap, GenerateConstellationMap, GenerateHashes


def GetMatchingHashes(
    connection,
    hashValue
):

    cursor = connection.cursor()

    query = """
    SELECT
        song_id,
        time_offset
    FROM fingerprints
    WHERE hash = %s
    """

    cursor.execute(
        query,
        (hashValue,)
    )

    matches = cursor.fetchall()

    cursor.close()

    return matches
def MatchHashes(connection, queryHashes):

    offsetCounts = {}

    for hashValue, queryTime in queryHashes:

        matches = GetMatchingHashes(
            connection,
            hashValue
        )

        for songID, dbOffset in matches:

            deltaOffset = (dbOffset - queryTime)

            key = (
                songID,
                deltaOffset
            )

            if key not in offsetCounts:

                offsetCounts[key] = 0

            offsetCounts[key] += 1

    return offsetCounts
def GetSongName(
    connection,
    songID
):

    cursor = connection.cursor()

    query = """
    SELECT song_name
    FROM songs
    WHERE id = %s
    """

    cursor.execute(
        query,
        (songID,)
    )

    result = cursor.fetchone()

    cursor.close()

    return result[0]
def BestMatch(connection,offsetCounts):

    bestSongID = None
    bestCount = 0

    for key, count in offsetCounts.items():

        songID, offset = key

        if count > bestCount:

            bestCount = count
            bestSongID = songID

    bestSongName = GetSongName(
        connection,
        bestSongID
    )

    return bestSongName, bestCount

def IdentifySong(connection, queryFile):
    queryConstellation = GenerateConstellationMap(queryFile)
    queryHashes = GenerateHashes(queryConstellation)
    
    print(f"Query hashes: {len(queryHashes)}")  # already have this
    
    offsetCounts = MatchHashes(connection, queryHashes)
    
    print(f"Total offset buckets: {len(offsetCounts)}")  # ← add this
    print(f"Top 5 matches: {sorted(offsetCounts.items(), key=lambda x: x[1], reverse=True)[:5]}")  # ← and this
    
    bestSong, bestCount = BestMatch(connection, offsetCounts)
    return bestSong, bestCount
