from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import cm


class Interactive(object):
    def __init__(self):
        self.fig, (self.ax, self.imax) = fig, (ax, imax) = \
            plt.subplots(1, 2, figsize=(10, 5), facecolor='white')
        self.canvas = canvas = fig.canvas

        self._init_controlaxis(ax)
        self._init_imageaxis(imax)

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)

    def _init_controlaxis(self, ax):
        ax.axis([-1,1,-1,1])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.autoscale(False)
        self.circle = circle = Circle(
            (0,0), radius=0.01, facecolor='r', animated=True)
        ax.add_patch(circle)
        self._dragging = False

    def _init_imageaxis(self, imax):
        imax.set_axis_off()
        self.A = np.random.randn(900,2)
        self.image = imax.imshow(np.random.randn(30,30), cmap=cm.YlGnBu)
        imax.autoscale(False)

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

        self.ax.draw_artist(self.circle)
        self.imax.draw_artist(self.image)

        self.canvas.blit(self.ax.bbox)
        self.canvas.blit(self.imax.bbox)

    def button_press_callback(self, event):
        if event.inaxes is None or event.button != 1:
            return

        self._dragging = True
        self._update(event.xdata, event.ydata)

    def button_release_callback(self, event):
        if event.button == 1:
            self._dragging = False

    def motion_notify_callback(self, event):
        if event.inaxes is not self.ax or event.button != 1:
            return
        if self._dragging:
            self._update(event.xdata, event.ydata)

    def _update(self, x, y):
        self._reposition_circle(x, y)
        self._update_image(x, y)

    def _reposition_circle(self, x, y):
        self.circle.center = x, y
        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.circle)
        self.canvas.blit(self.ax.bbox)

    def _update_image(self, x, y):
        self.image.set_data(self.A.dot((x,y)).reshape((30,30)))
        self.imax.draw_artist(self.image)
        self.canvas.blit(self.imax.bbox)


if __name__ == '__main__':
    v = Interactive()
    plt.show()
