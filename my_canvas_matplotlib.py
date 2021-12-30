from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class CanvasMatplotlib(FigureCanvasQTAgg):

    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(CanvasMatplotlib, self).__init__(self.fig)
        self.axes.format_coord = lambda x, y: '(x = ' + format(x, '1.4f') + ', \t' + ' y = ' + format(y, '1.4f') + ')'
        self.axes.grid(color='green', linestyle='--', linewidth=0.5)
        self.axes.yaxis.tick_left()  # enlève les traits de graduation sur le côté gauche du graphique
        self.axes.xaxis.tick_bottom()  # enlève les traits de graduation sur la partie supérieure du graphique
        self.axes.spines[['top', 'right']].set_color('none')
        self.add_arrows()

    def add_arrows(self):
        al = 8.  # arrow length in points
        arrowprops = dict(clip_on=True,  # plotting outside axes on purpose
                          # frac=1.,  # make end arrowhead the whole size of arrow
                          headwidth=5.,  # in points
                          facecolor='k')
        kwargs = dict(
            xycoords='axes fraction',
            textcoords='offset points',
            arrowprops=arrowprops,
        )
        self.axes.annotate("", (1, 0), xytext=(-al, 0), **kwargs)
        self.axes.annotate("", (0, 1), xytext=(0, -al), **kwargs)  # left spin arrow
