import pickle
from scipy.signal import butter, lfilter, freqz, fftconvolve, resample_poly

def StoreHashes(
    hashes,
    songName,
    database
):

    for hashValue, anchorTime in hashes:

        if hashValue not in database:

            database[hashValue] = []

        database[hashValue].append(
            (
                songName,
                anchorTime
            )
        )

    return database

def SaveDatabase(
    database,
    filename="fingerprintDatabase.pkl"
):

    with open(filename, "wb") as file:

        pickle.dump(
            database,
            file
        )

    print("\nDatabase Saved")

def LoadDatabase(
    filename="fingerprintDatabase.pkl"
):

    with open(filename, "rb") as file:

        database = pickle.load(file)

    print("\nDatabase Loaded")

    return database