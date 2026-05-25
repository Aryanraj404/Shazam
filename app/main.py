from fastapi import FastAPI

from app.audio.recorder import *

from app.database.db import *

from app.matching.matcher import *


app = FastAPI()

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
