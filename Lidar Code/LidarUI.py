import pygame
import math
from math import floor
from adafruit_rplidar import RPLidar
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QProgressBar, QFileDialog, QSlider
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import csv
import json
import numpy as np
from PyQt5.QtGui import QImage, QPainter

# Setup the RPLidar
PORT_NAME = "/dev/ttyUSB0"
lidar = RPLidar(None, PORT_NAME, timeout=3)

# Screen settings
WIDTH, HEIGHT = 800, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
MAX_DISTANCE = 4000  # Set according to your lidar's maximum range

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lidar Visualization")
clock = pygame.time.Clock()

# Colors
BACKGROUND_COLOR = (20, 20, 30)
POINT_COLOR = (255, 215, 0)  # Gold color for latest frame
GRID_COLOR = (50, 50, 70)
CIRCLE_COLOR = (100, 100, 150)

# Initialize data storage
scan_history = []  # Store recent scan frames
zoom_level = 1
scan_speed = 30  # Scan update speed (frames per second)


# Function to map lidar data to screen coordinates
def polar_to_cartesian(angle, distance, zoom_factor):
    if distance > MAX_DISTANCE:
        distance = MAX_DISTANCE
    angle_rad = math.radians(angle)
    x = CENTER_X + int(distance * math.cos(angle_rad) * (WIDTH / 2) / MAX_DISTANCE * zoom_factor)
    y = CENTER_Y + int(distance * math.sin(angle_rad) * (HEIGHT / 2) / MAX_DISTANCE * zoom_factor)
    return x, y


# Function to draw grid and circles for reference
def draw_grid(show_grid=True):
    screen.fill(BACKGROUND_COLOR)
    if show_grid:
        for r in range(500, WIDTH // 2, 500):
            pygame.draw.circle(screen, CIRCLE_COLOR, (CENTER_X, CENTER_Y), r, 1)
        for angle in range(0, 360, 45):
            x = CENTER_X + int((WIDTH // 2) * math.cos(math.radians(angle)))
            y = CENTER_Y + int((HEIGHT // 2) * math.sin(math.radians(angle)))
            pygame.draw.line(screen, GRID_COLOR, (CENTER_X, CENTER_Y), (x, y))


# Function to process and visualize data
def process_data():
    draw_grid(show_grid=True)  # Clear screen and draw grid

    # Draw each scan frame in the history
    for data in scan_history:
        for angle in range(360):
            distance = data[angle]
            if distance > 0:
                x, y = polar_to_cartesian(angle, distance, zoom_level)
                pygame.draw.circle(screen, POINT_COLOR, (x, y), 2)

    pygame.display.flip()  # Update display


# Worker thread for Lidar scanning
class LidarWorker(QThread):
    update_signal = pyqtSignal()
    status_signal = pyqtSignal(str)  # Signal for sending status messages

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        try:
            self.status_signal.emit("Scanning...")
            for scan in lidar.iter_scans():
                if not self.running:
                    break

                # Prepare scan data for this frame
                scan_data = [0] * 360
                for _, angle, distance in scan:
                    scan_data[min([359, floor(angle)])] = distance

                # Append current frame to history and keep only last 3 frames
                scan_history.append(scan_data)
                if len(scan_history) > 3:
                    scan_history.pop(0)

                # Trigger update signal to refresh the PyQt5 window
                self.update_signal.emit()

                clock.tick(scan_speed)  # Control the speed of scan updates

        except KeyboardInterrupt:
            print("Lidar stopped.")
        finally:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            self.status_signal.emit("Idle")


# Main UI for Lidar control
class LidarUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('LIDAR Control')

        layout = QVBoxLayout()

        # LIDAR ON/OFF Button
        self.toggle_button = QPushButton("Turn LIDAR ON")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_lidar)
        layout.addWidget(self.toggle_button)

        # Measure LIDAR distance button
        self.measure_button = QPushButton("Measure LIDAR Distance")
        self.measure_button.clicked.connect(self.measure_lidar)
        layout.addWidget(self.measure_button)

        # Scan Status Label
        self.status_label = QLabel("Idle")
        layout.addWidget(self.status_label)

        # Zoom Controls (Slider)
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(1, 5)
        self.zoom_slider.setValue(1)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        layout.addWidget(QLabel("Zoom Level"))
        layout.addWidget(self.zoom_slider)

        # Speed Control for Scanning (Slider)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 60)
        self.speed_slider.setValue(scan_speed)
        self.speed_slider.valueChanged.connect(self.update_speed)
        layout.addWidget(QLabel("Scan Speed (FPS)"))
        layout.addWidget(self.speed_slider)

        # Grid Toggle Button
        self.toggle_grid_button = QPushButton("Toggle Grid")
        self.toggle_grid_button.clicked.connect(self.toggle_grid)
        layout.addWidget(self.toggle_grid_button)

        # Clear Button
        self.clear_button = QPushButton("Clear Scan Data")
        self.clear_button.clicked.connect(self.clear_data)
        layout.addWidget(self.clear_button)

        # Save Data Button
        self.save_button = QPushButton("Save Scan Data")
        self.save_button.clicked.connect(self.save_scan_data)
        layout.addWidget(self.save_button)

        # Progress Bar for scanning
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        # Initialize Lidar worker thread
        self.lidar_worker = LidarWorker()
        self.lidar_worker.update_signal.connect(self.update_ui)
        self.lidar_worker.status_signal.connect(self.update_status)

        self.show()

    def toggle_lidar(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setText("Turn LIDAR OFF")
            self.lidar_worker.running = True
            self.lidar_worker.start()
        else:
            self.toggle_button.setText("Turn LIDAR ON")
            self.lidar_worker.running = False
            self.lidar_worker.quit()

    def measure_lidar(self):
        print("Measuring LIDAR distance...")

    def update_ui(self):
        # Update the pygame window on the PyQt interface
        process_data()
        pygame.display.update()

    def update_status(self, status):
        self.status_label.setText(status)

    def update_zoom(self):
        global zoom_level
        zoom_level = self.zoom_slider.value()

    def update_speed(self):
        global scan_speed
        scan_speed = self.speed_slider.value()

    def toggle_grid(self):
        global show_grid
        show_grid = not show_grid

    def clear_data(self):
        global scan_history
        scan_history = []
        print("Scan data cleared!")

    def save_scan_data(self):
        # Save scan data to a file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Scan Data", "", "JSON Files (*.json);;CSV Files (*.csv)", options=options)
        if file_path:
            if file_path.endswith('.json'):
                self.save_to_json(file_path)
            elif file_path.endswith('.csv'):
                self.save_to_csv(file_path)

    def save_to_json(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(scan_history, f, indent=4)
        print(f"Scan data saved to {file_path}")

    def save_to_csv(self, file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(scan_history)
        print(f"Scan data saved to {file_path}")


# Initialize PyQt5 application
def main():
    app = QApplication([])

    # Create Lidar UI
    lidar_ui = LidarUI()

    # Start PyQt5 event loop
    app.exec_()


if __name__ == "__main__":
    main()
