import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap

# Set the Qt platform plugin path explicitly (fixes the xcb error)
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/path/to/your/pyqt5/plugins/platforms'

# Simulate the thermal camera behavior with a mock function that raises the ValueError
class MockThermalCamera:
    def start_camera(self):
        raise ValueError("No I2C device at address: 0x33")  # Simulating the error

    def stop_camera(self):
        pass

    def get_current_frame(self):
        raise ValueError("No I2C device at address: 0x33")  # Simulating the error


# Define a new thread to handle thermal image capture and detection
class CaptureThread(QThread):
    new_frame_signal = pyqtSignal(np.ndarray)  # Signal to pass new frame to UI

    def __init__(self):
        super().__init__()
        self.camera_on = False

    def run(self):
        while self.camera_on:
            try:
                thermal_data = ptc.get_current_frame()  # Simulate the failure here
                self.new_frame_signal.emit(thermal_data)  # Emit signal with the frame
            except ValueError as e:
                print(f"Error: {e}")
                break  # Stop the thread on error
            self.msleep(100)  # Sleep to control frame rate (10 FPS)

    def start_capture(self):
        self.camera_on = True
        self.start()

    def stop_capture(self):
        self.camera_on = False
        self.wait()

class ThermalCameraUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Thermal Camera Control')

        # Layout for UI components
        layout = QVBoxLayout()
        self.image_label = QLabel(self)  # Label to show thermal image
        layout.addWidget(self.image_label)

        # Button to toggle camera on and off
        self.toggle_button = QPushButton("Turn Thermal Camera ON")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_camera)
        layout.addWidget(self.toggle_button)

        # Button to display thermal image
        self.image_button = QPushButton("Show Thermal Image")
        self.image_button.clicked.connect(self.show_thermal_image)
        layout.addWidget(self.image_button)

        # Button to start human detection
        self.detect_button = QPushButton("Detect Human")
        self.detect_button.clicked.connect(self.detect_human)
        layout.addWidget(self.detect_button)

        # Layout setup for the window
        self.setLayout(layout)

        self.camera_on = False
        self.capture_thread = CaptureThread()
        self.capture_thread.new_frame_signal.connect(self.display_image)  # Connect new frame signal

        # Using the MockThermalCamera to simulate no device error
        self.ptc = MockThermalCamera()  # Replace the actual `ptc` with a mock version

        # Load the pre-trained MobileNet SSD model for human detection
        self.net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

    def toggle_camera(self):
        """ Toggle the thermal camera on or off """
        if self.toggle_button.isChecked():
            self.toggle_button.setText("Turn Thermal Camera OFF")
            self.camera_on = True
            try:
                self.ptc.start_camera()  # This will simulate the error (No I2C device)
                self.capture_thread.start_capture()  # Start capturing frames
            except ValueError as e:
                print(f"Error: {e}")
                self.image_label.setText(str(e))  # Display the error in the GUI
        else:
            self.toggle_button.setText("Turn Thermal Camera ON")
            self.camera_on = False
            self.capture_thread.stop_capture()  # Stop capturing frames
            self.ptc.stop_camera()  # Stop the thermal camera

    def show_thermal_image(self):
        """ Display thermal image in the GUI """
        if self.camera_on:
            print("Displaying thermal image...")
            try:
                thermal_image = self.ptc.get_current_frame()  # This will simulate the error
                self.display_image(thermal_image)
            except ValueError as e:
                print(f"Error: {e}")
                self.image_label.setText(str(e))  # Display the error in the GUI
        else:
            print("Thermal camera is off. Please turn it on first.")

    def display_image(self, thermal_data):
        """ Display thermal image as a heatmap on PyQt5 QLabel """
        # Convert thermal data to a heatmap
        heatmap = cv2.applyColorMap(thermal_data, cv2.COLORMAP_JET)
        
        # Convert heatmap to QImage for display in PyQt5 QLabel
        height, width, channel = heatmap.shape
        bytes_per_line = 3 * width
        q_img = QImage(heatmap.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Show image on QLabel
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def detect_human(self):
        """ Detect human-like heat sources using deep learning model """
        if self.camera_on:
            print("Detecting human...")
            try:
                # Get the latest thermal frame
                thermal_data = self.ptc.get_current_frame()  # This will simulate the error
                # Resize the thermal image for input to MobileNet SSD (pre-trained model)
                frame_resized = cv2.resize(thermal_data, (300, 300))
                blob = cv2.dnn.blobFromImage(frame_resized, 1.0, (300, 300), (104, 117, 123), swapRB=False, crop=False)

                self.net.setInput(blob)
                detections = self.net.forward()

                # Draw bounding boxes around detected humans
                (h, w) = thermal_data.shape[:2]
                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence > 0.2:  # Set confidence threshold for human detection
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        cv2.rectangle(thermal_data, (startX, startY), (endX, endY), (255, 0, 0), 2)

                # Convert the image to a heatmap for display
                heatmap = cv2.applyColorMap(thermal_data, cv2.COLORMAP_JET)
                self.display_image(heatmap)  # Show the updated image with human detection
            except ValueError as e:
                print(f"Error: {e}")
                self.image_label.setText(str(e))  # Display the error in the GUI
        else:
            print("Turn on the camera first.")

if __name__ == '__main__':
    import sys

    # Initialize the PyQt application
    app = QApplication(sys.argv)

    # Create and show the UI
    window = ThermalCameraUI()
    window.show()

    # Run the application event loop
    sys.exit(app.exec_())
