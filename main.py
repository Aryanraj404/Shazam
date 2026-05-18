from audio.audiomodule import *
import matplotlib.pyplot as plt


def PlotConstellationMap(
    constellationMap
):

    x = [p[0] for p in constellationMap]
    y = [p[1] for p in constellationMap]

    plt.figure(figsize=(14,6))

    plt.scatter(
        x,
        y,
        s=1
    )

    plt.xlabel("Time Window")
    plt.ylabel("Frequency Bin")

    plt.title("Constellation Map")

    plt.show()


constellationMap = GenerateConstellationMap(
    "song1.wav"
)

print(constellationMap[:50])
print(len(constellationMap))

PlotConstellationMap(
    constellationMap
)