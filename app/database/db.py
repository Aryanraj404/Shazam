
from scipy.signal import butter, lfilter, freqz, fftconvolve, resample_poly
import psycopg2
import os

def ConnectToDatabase():
    return psycopg2.connect(os.environ["DATABASE_URL"])



def InsertSong(connection,songname):
    cursor = connection.cursor()

    query = """INSERT INTO songs(song_name) VALUES(%s) RETURNING id;"""
    cursor.execute(query,(songname,))

    songID = cursor.fetchone()[0]

    connection.commit()
    cursor.close()

    return songID

def InsertFingerprints(
    connection,
    hashes,
    songID
):

    cursor = connection.cursor()

    query = """
    INSERT INTO fingerprints(
        hash,
        song_id,
        time_offset
    )
    VALUES(%s,%s,%s)
    """

    for hashValue, anchorTime in hashes:

        cursor.execute(
            query,
            (
                hashValue,
                songID,
                anchorTime
            )
        )

    connection.commit()

    cursor.close()

def SongExists(
    connection,
    songName
):

    cursor = connection.cursor()

    query = """
    SELECT id
    FROM songs
    WHERE song_name = %s
    """

    cursor.execute(
        query,
        (songName,)
    )

    result = cursor.fetchone()

    cursor.close()

    return result