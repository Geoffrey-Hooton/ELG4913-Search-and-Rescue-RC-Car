import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Configurer I2C
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)

# Régler la fréquence PWM
pca.frequency = 50  # Fréquence standard pour les servos (50Hz)

# Choisir les canaux PWM pour les 4 servos
servo_channels = [pca.channels[0], pca.channels[1], pca.channels[2], pca.channels[3]]

# Fonction pour définir l'angle des servos
def set_servo_angle(channel, angle):
    pulse_width = int((angle / 180.0) * 1000 + 1000)
    pwm_value = int((pulse_width / 20000) * 65535)
    channel.duty_cycle = pwm_value

# Fonction pour arrêter un servo
def stop_servo(channel):
    channel.duty_cycle = 0

# Fonction pour faire tourner les 4 servos dans le même sens
def rotate_servos_same_direction_4(servo_channels):
    for angle in range(0, 181, 10):
        print(f"Déplacement de tous les servos à {angle} degrés")
        for i, channel in enumerate(servo_channels):
            print(f"  -> Servo {i+1} à {angle} degrés")
            set_servo_angle(channel, angle)
        time.sleep(0.5)
    print("Rotation complète pour 4 servos")

try:
    # Faire tourner les servos
    rotate_servos_same_direction_4(servo_channels)

    # Arrêter les servos
    print("Arrêt des servos")
    for channel in servo_channels:
        stop_servo(channel)

finally:
    pca.deinit()  # Nettoyer le PCA9685
