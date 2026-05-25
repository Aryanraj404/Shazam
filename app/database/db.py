
from scipy.signal import butter, lfilter, freqz, fftconvolve, resample_poly
import psycopg2


def ConnectToDatabase():

    connection = psycopg2.connect(
    host="localhost",
    database="sonichash",
    user ="aryan",
    password = "aryanKr_05")
    return connection



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