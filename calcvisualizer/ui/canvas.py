from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, width=10, height=12, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor("#f0f0f0")
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setMinimumSize(400, 300)
        self.fig.set_layout_engine("constrained")
        