import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from mplsoccer import Pitch

# Dane
titles = ["Pierwszy wykres", "Drugi wykres", "Trzeci wykres"]
colors = ['white', 'lightgreen', 'lightblue']

class PlotNavigator:
    def __init__(self, titles, colors):
        self.titles = titles
        self.colors = colors
        self.index = 0

        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(bottom=0.12)  # mniej miejsca pod wykresem

        # Mniejsze przyciski
        axprev = self.fig.add_axes([0.25, 0.02, 0.15, 0.06])  # [x, y, width, height]
        axnext = self.fig.add_axes([0.6, 0.02, 0.15, 0.06])
        self.bprev = Button(axprev, 'Previous')
        self.bnext = Button(axnext, 'Next')

        self.bprev.on_clicked(self.prev_plot)
        self.bnext.on_clicked(self.next_plot)

        self.plot_current()
        plt.show()

    def plot_current(self):
        self.ax.clear()
        pitch = Pitch(pitch_color=self.colors[self.index], line_color='black')
        pitch.draw(ax=self.ax)
        self.ax.set_title(self.titles[self.index])
        self.fig.canvas.draw_idle()

    def prev_plot(self, event):
        self.index = (self.index - 1) % len(self.titles)
        self.plot_current()

    def next_plot(self, event):
        self.index = (self.index + 1) % len(self.titles)
        self.plot_current()

# Uruchom
if __name__ == '__main__':
    PlotNavigator(titles, colors)