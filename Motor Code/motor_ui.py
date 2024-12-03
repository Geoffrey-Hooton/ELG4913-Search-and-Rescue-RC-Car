import sys
import time
import board
import busio
from adafruit_pca9685 import PCA9685
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

# Initialize I2C and PCA9685 for servo control
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard frequency for servos (50Hz)

# Assign channels to the 6 servos for movement and 1 for lifting
front_left_servo = pca.channels[0]
front_right_servo = pca.channels[1]
middle_left_servo = pca.channels[2]  # New motor
middle_right_servo = pca.channels[3]  # New motor
rear_left_servo = pca.channels[4]
rear_right_servo = pca.channels[5]
lifter_servo = pca.channels[6]

# Function to set servo speed
def set_servo_speed(channel, speed):
    if speed == 0:
        channel.duty_cycle = 0
    else:
        pulse_width = int((speed / 100.0) * 500 + 1500)  # -100 -> 1ms, 100 -> 2ms
        pwm_value = int((pulse_width / 20000) * 65535)
        channel.duty_cycle = pwm_value

# Define movement functions
def move_forward():
    print("La voiture avance")
    set_servo_speed(front_left_servo, 100)
    set_servo_speed(front_right_servo, 100)
    set_servo_speed(middle_left_servo, 100)
    set_servo_speed(middle_right_servo, 100)
    set_servo_speed(rear_left_servo, 100)
    set_servo_speed(rear_right_servo, 100)

def move_backward():
    print("La voiture recule")
    set_servo_speed(front_left_servo, -100)
    set_servo_speed(front_right_servo, -100)
    set_servo_speed(middle_left_servo, -100)
    set_servo_speed(middle_right_servo, -100)
    set_servo_speed(rear_left_servo, -100)
    set_servo_speed(rear_right_servo, -100)

def turn_left():
    print("La voiture tourne à gauche (pivot)")
    set_servo_speed(front_left_servo, -50)
    set_servo_speed(front_right_servo, 50)
    set_servo_speed(middle_left_servo, -50)
    set_servo_speed(middle_right_servo, 50)
    set_servo_speed(rear_left_servo, -50)
    set_servo_speed(rear_right_servo, 50)

def turn_right():
    print("La voiture tourne à droite (pivot)")
    set_servo_speed(front_left_servo, 50)
    set_servo_speed(front_right_servo, -50)
    set_servo_speed(middle_left_servo, 50)
    set_servo_speed(middle_right_servo, -50)
    set_servo_speed(rear_left_servo, 50)
    set_servo_speed(rear_right_servo, -50)

def stop_all():
    print("La voiture s'arrête")
    set_servo_speed(front_left_servo, 0)
    set_servo_speed(front_right_servo, 0)
    set_servo_speed(middle_left_servo, 0)
    set_servo_speed(middle_right_servo, 0)
    set_servo_speed(rear_left_servo, 0)
    set_servo_speed(rear_right_servo, 0)

def lift_object():
    print("Lever l'objet")
    set_servo_speed(lifter_servo, 100)

def lower_object():
    print("Abaisser l'objet")
    set_servo_speed(lifter_servo, -100)

def stop_lifter():
    print("Arrêter le lifter")
    set_servo_speed(lifter_servo, 0)

# MotorControlUI class
class MotorControlUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Motor Control')

        layout = QVBoxLayout()

        self.status_label = QLabel("Motor Status: Stopped")
        layout.addWidget(self.status_label)

        self.forward_button = QPushButton("Move Forward")
        self.forward_button.clicked.connect(self.move_forward)
        layout.addWidget(self.forward_button)

        self.backward_button = QPushButton("Move Backward")
        self.backward_button.clicked.connect(self.move_backward)
        layout.addWidget(self.backward_button)

        self.left_button = QPushButton("Turn Left")
        self.left_button.clicked.connect(self.turn_left)
        layout.addWidget(self.left_button)

        self.right_button = QPushButton("Turn Right")
        self.right_button.clicked.connect(self.turn_right)
        layout.addWidget(self.right_button)

        self.lift_button = QPushButton("Lift Object")
        self.lift_button.clicked.connect(self.lift_object)
        layout.addWidget(self.lift_button)

        self.lower_button = QPushButton("Lower Object")
        self.lower_button.clicked.connect(self.lower_object)
        layout.addWidget(self.lower_button)

        self.stop_button = QPushButton("Stop All")
        self.stop_button.clicked.connect(self.stop_all)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def move_forward(self):
        print("Motor moving forward...")
        move_forward()
        self.status_label.setText("Motor Status: Moving Forward")

    def move_backward(self):
        print("Motor moving backward...")
        move_backward()
        self.status_label.setText("Motor Status: Moving Backward")

    def turn_left(self):
        print("Motor turning left...")
        turn_left()
        self.status_label.setText("Motor Status: Turning Left")

    def turn_right(self):
        print("Motor turning right...")
        turn_right()
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

    def closeEvent(self, event):
        # Clean up PCA9685 on exit
        pca.deinit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MotorControlUI()
    window.show()
    sys.exit(app.exec_())
