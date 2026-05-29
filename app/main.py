from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.audio.recorder import *

from app.database.db import *

from app.matching.matcher import *
from fastapi import UploadFile, File
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

connection = ConnectToDatabase()


@app.get("/")
def home():

    return {
        "message": "Shazam Clone Backend Running"
    }


@app.post("/identify")
def identify_song():

    RecordAudio(
        "query/query.wav",
        8
    )

    bestSong, bestCount = IdentifySong(
        connection,
        "query/query.wav"
    )

    return {

        "detected_song": bestSong,

        "match_score": bestCount
    }
@app.post("/add-song")
async def add_song(
    song: UploadFile = File(...)
):

    connection.rollback()

    if SongExists(
        connection,
        song.filename
    ):
        return {
            "message": "⚠️ Song Already Exists"
        }

    songPath = os.path.join(
        "songs",
        song.filename
    )

    with open(
        songPath,
        "wb"
    ) as file:

        content = await song.read()
        file.write(content)

    songID = InsertSong(
        connection,
        song.filename
    )

    constellationMap = (
        GenerateConstellationMap(
            songPath
        )
    )

    hashes = GenerateHashes(
        constellationMap
    )

    InsertFingerprints(
        connection,
        hashes,
        songID
    )

    return {
        "message": " Song Added Successfully",
        "song": song.filename,
        "hashes": len(hashes)
    }