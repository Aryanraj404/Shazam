import os

from app.audio.fingerprint import *
from app.audio.recorder import *
from app.database.db import *
from app.matching.matcher import *


DATABASE_FILE = "fingerprintDatabase.pkl"


# =========================
# LOAD OR BUILD DATABASE
# =========================

if os.path.exists(DATABASE_FILE):

    database = LoadDatabase(
        DATABASE_FILE
    )

else:

    print("\nBuilding Fingerprint Database...\n")

    database = {}

    songsFolder = "songs"

    for songFile in os.listdir(songsFolder):

        if not songFile.endswith(".wav"):
            continue

        songPath = (
            songsFolder
            +
            "/"
            +
            songFile
        )

        print(
            f"Processing {songFile}..."
        )

        constellationMap = (
            GenerateConstellationMap(
                songPath
            )
        )

        hashes = GenerateHashes(
            constellationMap
        )

        database = StoreHashes(
            hashes,
            songFile,
            database
        )

        print(
            f"{songFile} -> {len(hashes)} hashes"
        )

    SaveDatabase(
        database,
        DATABASE_FILE
    )

    print("\nDatabase Ready")


# =========================
# RECORD QUERY AUDIO
# =========================

RecordAudio(
    "query/query.wav",
    8
)


# =========================
# GENERATE QUERY HASHES
# =========================

queryConstellation = (
    GenerateConstellationMap(
        "query/query.wav"
    )
)

queryHashes = GenerateHashes(
    queryConstellation
)


# =========================
# MATCH AGAINST DATABASE
# =========================

offsetCounts = MatchHashes(
    queryHashes,
    database
)


# =========================
# BEST MATCH
# =========================

bestSong, bestCount = BestMatch(
    offsetCounts
)


print("\n====================")
print("Detected Song:")
print(bestSong)

print("\nMatch Score:")
print(bestCount)
print("====================\n")