import numpy as np
from matplotlib import pyplot as plt
import re

from matplotlib.pyplot import imshow, show

naturals = [5, 0, 7, 2, 9, 4]
flats = [10, 3, 8, 1, 6]
sharps = [6, 1, 8, 3, 10]
sharp = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'h']
flat = ['c', 'des', 'd', 'es', 'e', 'f', 'ges', 'g', 'as', 'a', 'b', 'h']

accidentals = []


def load(var):
    score = []
    with open(var, "r") as variation:
        bars = variation.readlines()
        for index, bar in enumerate(bars):
            if index == len(bars) / 2:
                break
            b = [clean(bar.strip("\n")), clean(bars[index + (len(bars)//2)].strip("\n"))]
            score.append(b[0] + b[1])
    accidentals_per_bar(score)


def accidentals_per_bar(score):
    degrees = []
    for bar in score:
        bar = list(set(bar))
        chromatic_degree = 0
        for pitch in bar:
            if pitch in flat:
                transposed_pitch = (flat.index(pitch) - 7) % 12
                if transposed_pitch in flats:
                    chromatic_degree += flats.index(transposed_pitch) + 1
            elif pitch in sharp:
                transposed_pitch = (sharp.index(pitch) - 7) % 12
                if transposed_pitch in sharps:
                    chromatic_degree += sharps.index(transposed_pitch) + 1
        degrees.append(chromatic_degree)
    accidentals.append(degrees)


def plots():
    plt.plot(accidentals[0], label="Var. 1")
    plt.plot(accidentals[1], label="Var. 2")
    plt.plot(accidentals[2], label="Var. 4")
    plt.legend(loc="upper left")
    plt.xticks(np.arange(len(accidentals[1])), np.arange(1, len(accidentals[1]) + 1))
    plt.xlabel("Takt")
    plt.ylabel("Chromatik")
    plt.grid()
    plt.show()


def make_image(nbars):
    img = np.empty((nbars, nbars, 3), dtype=np.uint8)
    img.fill(255)
    divisor = int(255 / max(accidentals[0]))
    print(img.ndim)
    for index, row in enumerate(img):
        for pixel in row:
            pixel[1] = accidentals[0][index] * divisor
            pixel[2] = 0

    img = img.repeat(10, axis=0).repeat(10, axis=1)
    imshow(img, interpolation="nearest")
    show()
    plt.imsave("var4.png", img)


def clean(bar):
    b = re.sub(r'[^a-zA-Z\s\n]', u'', bar, flags=re.UNICODE)
    b = b.split(' ')
    b = [c for c in b if c in sharp or c in flat]
    return b


if __name__ == "__main__":
    number_of_bars = 34
    goldberg_variationen = ["var1", "var2", "var4"]
    for var in goldberg_variationen:
        load(var)
    plots()
    #make_image(number_of_bars)
