# reference: https://gist.github.com/saketkc/45559a011a354a9cca2fbe4e208dde61
import seaborn
import matplotlib.pyplot as plt

plt.style.use('seaborn-ticks')
from matplotlib import transforms, patheffects
import matplotlib.patheffects
import numpy as np

class Scale:
    def __init__(self, sx, sy=None):
        self._sx = sx
        self._sy = sy

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        affine = affine.identity().scale(self._sx, self._sy) + affine
        renderer.draw_path(gc, tpath, affine, rgbFace)

def draw_logo(color_scores,colors):
        fig = plt.figure()
        radio_inch=5/2;
        color_scores_length = len(color_scores)
        fig.set_size_inches(color_scores_length, radio_inch)
        ax = fig.add_subplot(111)
        ax.set_xticks(range(color_scores_length))

        x_to_increase = 0

        for scores in color_scores:
            y_to_increase = 0
            for base, score in scores:
                txt = plt.text(x_to_increase, y_to_increase, base, fontsize=64, color=colors[base])
                txt.set_path_effects([Scale(1.0, score)])
                fig.canvas.draw()
                y_to_increase += score*0.3
            x_to_increase += 1;

        ax.set_yticks(range(0, 3))
        seaborn.despine(ax=ax, offset=30, trim=True)
        ax.set_xticklabels(range(1, len(color_scores) + 1), rotation=90)
        ax.set_yticklabels(np.arange(0, 3, 1))
        plt.show()

class logo():
    colors = {'G': 'yellow',
              'A': 'Green',
              'C': 'blue',
              'T': 'red'}
    Bases = 'A','G','C','T'
    def _initi_(self,sx,sy):
        self.sx = sx
        self.sy = sy

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        affine = affine.identity().scale(self._sx, self._sy) + affine
        renderer.draw_path(gc, tpath, affine, rgbFace)



    color_scores = [[('A', 0.45),
                    ('G', 0.75),
                    ('C', 1.38),
                    ('T', 1.48), ],
                   [('T', 0.45),
                    ('A', 1.14),
                    ('G', 1.38),
                    ('C', 1.38)],
                   [('T', 0.11),
                    ('G', 2.02),
                    ('C', 2.02),
                    ('A', 0.79)],
                   [('A', 0.11),
                    ('G', 0.11),
                    ('T', 0.11),
                    ('C', 5.19)],
                   [('G', 0.11),
                    ('T', 0.11),
                    ('C', 0.11),
                    ('A', 2.85)],
                   [('G', 0.11),
                    ('A', 0.11),
                    ('T', 0.11),
                    ('C', 5.19)],
                   [('A', 0.11),
                    ('T', 0.11),
                    ('C', 0.11),
                    ('G', 5.19)],
                   [('C', 0.11),
                    ('G', 0.11),
                    ('A', 0.11),
                    ('T', 2.85)],
                   [('A', 0.11),
                    ('C', 0.11),
                    ('T', 1.14),
                    ('G', 3.29)],
                   [('A', 0.11),
                    ('T', 0.79),
                    ('C', 1.38),
                    ('G', 2.65)],
                   [('C', 0.11),
                    ('A', 0.45),
                    ('T', 0.79),
                    ('G', 3.29)],
                   [('A', 0.79),
                    ('T', 0.79),
                    ('C', 1.38),
                    ('G', 1.38)],

                   ]
    draw_logo(color_scores, colors);


