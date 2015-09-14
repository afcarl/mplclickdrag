from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import cm


# TODO image doens't get updated

class Interactive(object):
    def __init__(self, initial_point):
        self.fig, (ax, imax) = plt.subplots(2, 1, figsize=(5, 10), facecolor='white')
        self.canvas = canvas = self.fig.canvas

        # set up clicking subplot

        self.ax = ax
        ax.set_axis_off()
        ax.axis([-1,1,-1,1])
        ax.autoscale(False)

        self.circle = Circle(
            initial_point, radius=0.01, facecolor='r', animated=True)
        ax.add_patch(self.circle)

        self._dragging = False

        # set up image subplot

        self.imax = imax
        imax.set_axis_off()
        self.A = np.random.randn(900,2)
        self.image = imax.imshow(np.random.randn(30,30), cmap=cm.YlGnBu)
        imax.autoscale(False)

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)

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
        self._reposition_circle(event.xdata, event.ydata)
        self._update_image()

    def button_release_callback(self, event):
        if event.button == 1:
            self._dragging = False

    def motion_notify_callback(self, event):
        if event.inaxes is not self.ax or event.button != 1:
            return
        if self._dragging:
            self._reposition_circle(event.xdata, event.ydata)
            self._update_image()

    def _reposition_circle(self, x, y):
        self.circle.center = x, y
        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.circle)
        self.canvas.blit(self.ax.bbox)

    def _update_image(self):
        x, y = self.circle.center
        self.image.set_data(self.A.dot((x,y)).reshape((30,30)))
        self.imax.draw_artist(self.image)
        self.canvas.blit(self.imax.bbox)


if __name__ == '__main__':
    v = Interactive((0,0))
    plt.show()
