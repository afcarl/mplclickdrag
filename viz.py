from __future__ import division
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class Interactive(object):
    def __init__(self, initial_point):
        self.fig = fig = plt.figure(figsize=(5,5))
        self.canvas = canvas = fig.canvas
        self.ax = ax = plt.subplot(111)

        ax.axis([-1,1,-1,1])

        self.circle = Circle(
            initial_point, radius=0.01, facecolor='r', animated=True)
        ax.add_patch(self.circle)

        self._dragging = False

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)
        self.ax.draw_artist(self.circle)
        self.canvas.blit(self.fig.bbox)

    def button_press_callback(self, event):
        if event.inaxes is None or event.button != 1:
            return

        self._dragging = True
        self._reposition_circle(event.xdata, event.ydata)

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
        self.canvas.blit(self.fig.bbox)


if __name__ == '__main__':
    v = Interactive((0,0))
    plt.show()
