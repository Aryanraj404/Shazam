from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.audio.recorder import *
from pydub import AudioSegment
from app.database.db import *

from app.matching.matcher import *
from fastapi import UploadFile, File
import uuid, os

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
async def identify_song(audio: UploadFile = File(...)):
    uid = uuid.uuid4().hex
    rawPath = f"query/query_{uid}.webm"
    wavPath = f"query/query_{uid}.wav"

    with open(rawPath, "wb") as f:
        f.write(await audio.read())

    try:
        # Force 44100 Hz mono before fingerprinting
        sound = AudioSegment.from_file(rawPath)
        sound = sound.set_frame_rate(44100).set_channels(1)
        sound.export(wavPath, format="wav")

        bestSong, bestCount = IdentifySong(connection, wavPath)

        if not bestSong or bestCount < 20:
            return {"detected_song": "No match found", "match_score": bestCount}

        return {"detected_song": bestSong, "match_score": bestCount}

    finally:
        if os.path.exists(rawPath): os.remove(rawPath)
        if os.path.exists(wavPath): os.remove(wavPath)
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