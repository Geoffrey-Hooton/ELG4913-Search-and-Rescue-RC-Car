import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Configure I2C
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)

# Set PWM frequency for the servos
pca.frequency = 50  # Standard frequency for servos (50Hz)

# Assign channels to the 6 servos for car movement
front_left_servo = pca.channels[0]
front_right_servo = pca.channels[1]
middle_left_servo = pca.channels[2]
middle_right_servo = pca.channels[3]
rear_left_servo = pca.channels[4]
rear_right_servo = pca.channels[5]

# Assign the channel for the 7th servo (lifter)
lifter_servo = pca.channels[6]

# Function to set the speed or direction of a servo
def set_servo_speed(channel, speed):
    """
    Sets the speed of the servo based on the `speed` value.
    `speed` ranges from -100 (backward/lower) to 100 (forward/raise).
    """
    if speed == 0:  # Stop the servo
        channel.duty_cycle = 0
    else:
        # Convert speed (-100 to 100) into PWM duty cycle
        pulse_width = int((speed / 100.0) * 500 + 1500)  # -100 -> 1ms, 100 -> 2ms
        pwm_value = int((pulse_width / 20000) * 65535)
        channel.duty_cycle = pwm_value

# Function to move forward
def move_forwardspeed2():
    print("The car is moving forward")
    for servo in [front_left_servo, front_right_servo, middle_left_servo, middle_right_servo, rear_left_servo, rear_right_servo]:
        set_servo_speed(servo, 100)

def move_forwardspeed1():
    print("The car is moving forward")
    for servo in [front_left_servo, front_right_servo, middle_left_servo, middle_right_servo, rear_left_servo, rear_right_servo]:
        set_servo_speed(servo, 50)
# Function to move backward
def move_backwardspeed2():
    print("The car is moving backward")
    for servo in [front_left_servo, front_right_servo, middle_left_servo, middle_right_servo, rear_left_servo, rear_right_servo]:
        set_servo_speed(servo, -100)

def move_backwardspeed1():
    print("The car is moving backward")
    for servo in [front_left_servo, front_right_servo, middle_left_servo, middle_right_servo, rear_left_servo, rear_right_servo]:
        set_servo_speed(servo, -50)

# Function to turn left (pivot)
def turn_left():
    print("The car is turning left (pivot)")
    for servo in [front_left_servo, middle_left_servo, rear_left_servo]:
        set_servo_speed(servo, -50)
    for servo in [front_right_servo, middle_right_servo, rear_right_servo]:
        set_servo_speed(servo, 50)

# Function to turn right (pivot)
def turn_right():
    print("The car is turning right (pivot)")
    for servo in [front_left_servo, middle_left_servo, rear_left_servo]:
        set_servo_speed(servo, 50)
    for servo in [front_right_servo, middle_right_servo, rear_right_servo]:
        set_servo_speed(servo, -50)

# Function for a gentle curve to the left
def gentle_curve_left():
    print("The car is gently curving left")
    set_servo_speed(front_left_servo, 50)
    set_servo_speed(middle_left_servo, 50)
    set_servo_speed(rear_left_servo, 50)
    set_servo_speed(front_right_servo, 100)
    set_servo_speed(middle_right_servo, 100)
    set_servo_speed(rear_right_servo, 100)

# Function for a gentle curve to the right
def gentle_curve_right():
    print("The car is gently curving right")
    set_servo_speed(front_left_servo, 100)
    set_servo_speed(middle_left_servo, 100)
    set_servo_speed(rear_left_servo, 100)
    set_servo_speed(front_right_servo, 50)
    set_servo_speed(middle_right_servo, 50)
    set_servo_speed(rear_right_servo, 50)

# Function to stop all servos
def stop_all():
    print("The car is stopping")
    for servo in [front_left_servo, front_right_servo, middle_left_servo, middle_right_servo, rear_left_servo, rear_right_servo]:
        set_servo_speed(servo, 0)

# Function to lift the object with the 7th servo
def lift_object():
    print("Lifting the object")
    set_servo_speed(lifter_servo, 100)  # Raise the object

# Function to lower the object with the 7th servo
def lower_object():
    print("Lowering the object")
    set_servo_speed(lifter_servo, -100)  # Lower the object

# Function to stop the lifter servo
def stop_lifter():
    print("Stopping the lifter")
    set_servo_speed(lifter_servo, 0)  # Stop the lifter

# Test sequence
try:
    move_forwardspeed2()
    time.sleep(2)  # Move forward maximum speed for 2 seconds
    
    move_forwardspeed1()
    time.sleep(2) # Move forward normal speed for 2 seconds

    move_backwardspeed2()
    time.sleep(2)  # Move backward maximum speed for 2 seconds

    move_backwardspeed1()
    time.sleep(2)  # Move backward normal speed for 2 seconds
    
    turn_left()
    time.sleep(2)  # Turn left for 2 seconds

    turn_right()
    time.sleep(2)  # Turn right for 2 seconds

    gentle_curve_left()
    time.sleep(2)  # Gentle left curve for 2 seconds

    gentle_curve_right()
    time.sleep(2)  # Gentle right curve for 2 seconds

    lift_object()
    time.sleep(2)  # Lift the object for 2 seconds

    lower_object()
    time.sleep(2)  # Lower the object for 2 seconds

    stop_lifter()  # Stop the lifter
    stop_all()  # Stop the car

    print("Sequence completed")

finally:
    pca.deinit()  # Clean up the PCA9685