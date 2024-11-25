import matplotlib
matplotlib.use('QtAgg')  # Ensure the QtAgg backend is set before importing pyplot

import sys
import time
import Adafruit_ADS1x15
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process, Queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

# Create an ADS1115 ADC (16-bit) instance
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Choose a gain for reading voltages (16 = +/-0.256V)
GAIN = 16

# Graph settings
x_len = 500  # Number of points to display
y_range = [-750, 750]  # Y-axis range

# Sampling rate control (approximately 25 samples per second)
sampling_interval = 0.04  # In seconds (25Hz)

# Function to generate data
def generate_data(queue):
    """Simulate data collection from the ADC."""
    while True:
        value = adc.read_adc_difference(0, gain=GAIN)
        queue.put(value)
        time.sleep(sampling_interval)  # Control the sampling rate to 25Hz

# Function to animate the plot
def animate(i, ys, queue, line):
    if not queue.empty():
        value = queue.get()  # Get new data from the queue
        ys.append(value)
    
    ys = ys[-x_len:]  # Limit to x_len number of data points
    
    # Update the line with new Y values
    line.set_ydata(ys)
    
    return line,

# Main window with live graph
class GeophoneVisualization(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the PyQt5 UI
        self.setWindowTitle('Geophone Data Visualization')
        self.setGeometry(100, 100, 800, 600)
        
        # Set up the layout and widget
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        # Create the figure and axis for the plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(y_range)
        self.ax.set_title('Geophone Data')
        self.ax.set_xlabel('Data Points (Approximately 25 Readings each Second)')
        self.ax.set_ylabel('Voltage Value Post Gain Adjustment')

        # Initialize data
        self.xs = list(range(0, x_len))
        self.ys = [0] * x_len
        self.line, = self.ax.plot(self.xs, self.ys)

        # Set up the queue for multiprocessing
        self.queue = Queue()
        
        # Start the data generation process in a separate process
        self.p = Process(target=generate_data, args=(self.queue,))
        self.p.daemon = True  # Allow the process to exit when the main program exits
        self.p.start()

        # Set up FuncAnimation for live updates
        self.ani = animation.FuncAnimation(self.fig, animate, fargs=(self.ys, self.queue, self.line), interval=50, blit=True)

        # Embed the plot into the PyQt5 window
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # Import this here
        self.canvas = FigureCanvasQTAgg(self.fig)
        layout.addWidget(self.canvas)

        # Set up a timer to periodically update the UI and process events
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(50)  # 50ms for smooth UI updates

        self.show()

    def update_ui(self):
        """Periodically updates the UI and processes events."""
        QApplication.processEvents()  # Allow UI to process events (keep the UI responsive)
        self.canvas.draw()  # Redraw the canvas to show the updated plot

    def closeEvent(self, event):
        """Override close event to stop the data generation process"""
        self.p.terminate()
        self.p.join()
        event.accept()

if __name__ == "__main__":
    # Create the application and main window
    app = QApplication(sys.argv)
    window = GeophoneVisualization()
    sys.exit(app.exec_())
