import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider
from PyQt5.QtCore import Qt

# Simulate servo control (no actual hardware interaction)
def set_servo_speed(channel, speed):
    print(f"Setting servo on channel {channel} to speed {speed}")

# Define movement functions (simulated)
def move_forward(speed):
    print(f"La voiture avance à vitesse {speed}")
    for i in range(6):  # Simulating 6 servos
        set_servo_speed(i, speed)

def move_backward(speed):
    print(f"La voiture recule à vitesse {speed}")
    for i in range(6):  # Simulating 6 servos
        set_servo_speed(i, -speed)

def turn_left(speed):
    print(f"La voiture tourne à gauche (pivot) à vitesse {speed}")
    for i in range(6):  # Simulating 6 servos
        set_servo_speed(i, speed if i % 2 == 0 else -speed)

def turn_right(speed):
    print(f"La voiture tourne à droite (pivot) à vitesse {speed}")
    for i in range(6):  # Simulating 6 servos
        set_servo_speed(i, -speed if i % 2 == 0 else speed)

def stop_all():
    print("La voiture s'arrête")
    for i in range(6):  # Simulating 6 servos
        set_servo_speed(i, 0)

def lift_object():
    print("Lever l'objet")
    set_servo_speed(6, 100)  # Simulate lifting with the 7th servo

def lower_object():
    print("Abaisser l'objet")
    set_servo_speed(6, -100)  # Simulate lowering with the 7th servo

def stop_lifter():
    print("Arrêter le lifter")
    set_servo_speed(6, 0)  # Simulate stopping the lifter servo

# MotorControlUI class
class MotorControlUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Motor Control')

        # Initialize the speed slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)  # Set range for the speed
        self.slider.setValue(50)  # Default speed is 50
        self.slider.valueChanged.connect(self.update_speed)

        # Label to display the current speed
        self.speed_label = QLabel("Speed: 50", self)

        # Layout for buttons and speed control
        layout = QVBoxLayout()

        self.status_label = QLabel("Motor Status: Stopped")
        layout.addWidget(self.status_label)

        self.forward_button = QPushButton("Move Forward (W)")
        self.forward_button.clicked.connect(self.move_forward)
        layout.addWidget(self.forward_button)

        self.backward_button = QPushButton("Move Backward (S)")
        self.backward_button.clicked.connect(self.move_backward)
        layout.addWidget(self.backward_button)

        self.left_button = QPushButton("Turn Left (A)")
        self.left_button.clicked.connect(self.turn_left)
        layout.addWidget(self.left_button)

        self.right_button = QPushButton("Turn Right (D)")
        self.right_button.clicked.connect(self.turn_right)
        layout.addWidget(self.right_button)

        self.lift_button = QPushButton("Lift Object (1)")
        self.lift_button.clicked.connect(self.lift_object)
        layout.addWidget(self.lift_button)

        self.lower_button = QPushButton("Lower Object (2)")
        self.lower_button.clicked.connect(self.lower_object)
        layout.addWidget(self.lower_button)

        self.stop_button = QPushButton("Stop All (Backspace)")
        self.stop_button.clicked.connect(self.stop_all)
        layout.addWidget(self.stop_button)

        # Add the slider and its label to the layout
        layout.addWidget(self.speed_label)
        layout.addWidget(self.slider)

        self.setLayout(layout)

        # To track if the movement keys are pressed
        self.key_states = {
            Qt.Key_W: False,  # Move forward
            Qt.Key_S: False,  # Move backward
            Qt.Key_A: False,  # Turn left
            Qt.Key_D: False,  # Turn right
            Qt.Key_1: False,  # Lift object
            Qt.Key_2: False,  # Lower object
            Qt.Key_Backspace: False  # Stop all
        }

    def update_speed(self):
        # Update the displayed speed value
        speed = self.slider.value()
        self.speed_label.setText(f"Speed: {speed}")
        print(f"Speed changed to: {speed}")

    def move_forward(self):
        speed = self.slider.value()
        print(f"Motor moving forward at speed {speed}...")
        move_forward(speed)
        self.status_label.setText("Motor Status: Moving Forward")

    def move_backward(self):
        speed = self.slider.value()
        print(f"Motor moving backward at speed {speed}...")
        move_backward(speed)
        self.status_label.setText("Motor Status: Moving Backward")

    def turn_left(self):
        speed = self.slider.value()
        print(f"Motor turning left at speed {speed}...")
        turn_left(speed)
        self.status_label.setText("Motor Status: Turning Left")

    def turn_right(self):
        speed = self.slider.value()
        print(f"Motor turning right at speed {speed}...")
        turn_right(speed)
        self.status_label.setText("Motor Status: Turning Right")

    def lift_object(self):
        print("Lifting object...")
        lift_object()
        self.status_label.setText("Motor Status: Lifting Object")

    def lower_object(self):
        print("Lowering object...")
        lower_object()
        self.status_label.setText("Motor Status: Lowering Object")

    def stop_all(self):
        print("Stopping all motors and lifters...")
        stop_all()
        stop_lifter()
        self.status_label.setText("Motor Status: Stopped")

    def wheelEvent(self, event):
        # Override the wheel event to control the slider with mouse scroll
        delta = event.angleDelta().y()  # Positive for scroll up, negative for scroll down
        current_value = self.slider.value()
        if delta > 0 and current_value < 100:
            new_value = current_value + 1
            self.slider.setValue(new_value)  # Scroll up
        elif delta < 0 and current_value > 0:
            new_value = current_value - 1
            self.slider.setValue(new_value)  # Scroll down

    def keyPressEvent(self, event):
        # Handle key press events for movement and other actions
        speed = self.slider.value()  # Get the current speed value
        if event.key() == Qt.Key_W:
            self.key_states[Qt.Key_W] = True
            move_forward(speed)  # Call without self
            self.status_label.setText("Motor Status: Moving Forward")
        elif event.key() == Qt.Key_S:
            self.key_states[Qt.Key_S] = True
            move_backward(speed)  # Call without self
            self.status_label.setText("Motor Status: Moving Backward")
        elif event.key() == Qt.Key_A:
            self.key_states[Qt.Key_A] = True
            turn_left(speed)  # Call without self
            self.status_label.setText("Motor Status: Turning Left")
        elif event.key() == Qt.Key_D:
            self.key_states[Qt.Key_D] = True
            turn_right(speed)  # Call without self
            self.status_label.setText("Motor Status: Turning Right")
        elif event.key() == Qt.Key_1:
            self.key_states[Qt.Key_1] = True
            lift_object()  # Lift object
            self.status_label.setText("Motor Status: Lifting Object")
        elif event.key() == Qt.Key_2:
            self.key_states[Qt.Key_2] = True
            lower_object()  # Lower object
            self.status_label.setText("Motor Status: Lowering Object")
        elif event.key() == Qt.Key_Backspace:
            self.key_states[Qt.Key_Backspace] = True
            stop_all()  # Stop all actions
            self.status_label.setText("Motor Status: Stopped")
        event.accept()  # Ensure the event is properly handled

    def keyReleaseEvent(self, event):
        # Handle key release events to stop the action when key is released
        if event.key() == Qt.Key_W:
            self.key_states[Qt.Key_W] = False
            stop_all()
            self.status_label.setText("Motor Status: Stopped")
        elif event.key() == Qt.Key_S:
            self.key_states[Qt.Key_S] = False
            stop_all()
            self.status_label.setText("Motor Status: Stopped")
        elif event.key() == Qt.Key_A:
            self.key_states[Qt.Key_A] = False
            stop_all()
            self.status_label.setText("Motor Status: Stopped")
        elif event.key() == Qt.Key_D:
            self.key_states[Qt.Key_D] = False
            stop_all()
            self.status_label.setText("Motor Status: Stopped")
        elif event.key() == Qt.Key_1:
            self.key_states[Qt.Key_1] = False
            stop_lifter()
            self.status_label.setText("Motor Status: Stopped")
        elif event.key() == Qt.Key_2:
            self.key_states[Qt.Key_2] = False
            stop_lifter()
            self.status_label.setText("Motor Status: Stopped")
        elif event.key() == Qt.Key_Backspace:
            self.key_states[Qt.Key_Backspace] = False
            stop_all()
            self.status_label.setText("Motor Status: Stopped")
        event.accept()  # Ensure the event is properly handled

# Main program to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotorControlUI()
    window.show()
    sys.exit(app.exec_())
