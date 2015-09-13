from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class Interactive(object):
    epsilon = 5.  # pixel tolerance for click

    def __init__(self, fig, ax, initial_point):
        self.ax = ax
        self.canvas = canvas = fig.canvas

        self.circle = Circle(initial_point, radius=0.1, facecolor='r', alpha=0.5, animated=True)
        ax.add_patch(self.circle)

        self._dragging = False

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.circle)
        self.canvas.blit(self.ax.bbox)

    def button_press_callback(self, event):
        if event.inaxes is None or event.button != 1:
            return

        x, y = self.circle.center
        xc, yc = event.xdata, event.ydata

        if np.sqrt((x-xc)**2 + (y-yc)**2) < self.epsilon:
            self._reposition_circle(xc, yc)
            self._dragging = True

    def button_release_callback(self, event):
        if event.button == 1:
            self._dragging = False

    def motion_notify_callback(self, event):
        if event.inaxes is None or event.button != 1:
            return
        if self._dragging:
            self._reposition_circle(event.xdata, event.ydata)

    def _reposition_circle(self, x, y):
        self.circle.center = x, y
        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.circle)
        self.canvas.blit(self.ax.bbox)


if __name__ == '__main__':
    fig = plt.figure(figsize=(5,5))
    ax = plt.subplot(111)

    v = Interactive(fig, ax, (0,0))

    ax.set_xlim((-6,6))
    ax.set_ylim((-6,6))

    plt.show()
