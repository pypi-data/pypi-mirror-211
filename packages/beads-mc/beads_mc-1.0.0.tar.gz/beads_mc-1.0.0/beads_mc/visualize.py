
import matplotlib.pyplot as plt
import numpy as np
from .utils import line2cline
from PIL import Image


def plot_traitValues(trait_values, s=10):
    for rgba in trait_values:
        print(rgba)
        image = Image.new("RGBA", (s, s), rgba)
        image.show()


"""Visualize: beads_mc"""


def plot_beads(cline, ax=None, csize=0.4):
    if ax is None:
        fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)

    for i, color in enumerate(cline):
        x = i + 0.5
        y = 0.5
        ax.add_patch(plt.Circle((x, y), csize, color=color))

    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


def plot__linesASbeads(lineAB_samples):
    fig, AX = plt.subplots(len(lineAB_samples))
    for i, sample in enumerate(lineAB_samples):
        cline = line2cline(sample)
        plot_beads(cline, ax=AX[i])
    return fig, AX
