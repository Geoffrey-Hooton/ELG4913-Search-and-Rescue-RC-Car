import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Configurer I2C
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)

# Régler la fréquence PWM pour les servos
pca.frequency = 50  # Fréquence standard pour les servomoteurs (50Hz)

# Choisir les canaux PWM pour les 3 servomoteurs
servo_channels = [pca.channels[0], pca.channels[1], pca.channels[2]]  # Canaux 0, 1 et 2

# Fonction pour définir l'angle d'un servo
def set_servo_angle(channel, angle):
    # Convertir l'angle (0-180 degrés) en largeur d'impulsion PWM (spécifique au servo)
    pulse_width = int((angle / 180.0) * 1000 + 1000)  # 1ms pour 0° et 2ms pour 180°
    pwm_value = int((pulse_width / 20000) * 65535)  # Conversion en 16 bits
    channel.duty_cycle = pwm_value  # Régler le cycle de service PWM

# Fonction pour arrêter un servo
def stop_servo(channel):
    channel.duty_cycle = 0  # Mettre le cycle de service à zéro pour désactiver le signal

# Fonction pour faire tourner les 3 servos dans le même sens
def rotate_servos_same_direction_3(servo_channels):
    for angle in range(0, 181, 10):  # Faire varier l'angle de 0 à 180 avec un pas de 10
        print(f"Déplacement de tous les servos à {angle} degrés")
        for i, channel in enumerate(servo_channels):
            print(f"  -> Servo {i+1} à {angle} degrés")
            set_servo_angle(channel, angle)  # Appliquer l'angle à chaque servo
        time.sleep(0.5)  # Pause pour voir le mouvement
    print("Rotation complète des servos dans le même sens")

try:
    # Faire tourner les 3 servos dans le même sens
    rotate_servos_same_direction_3(servo_channels)

    # Arrêter tous les servos
    print("Arrêt des servos")
    for channel in servo_channels:
        stop_servo(channel)  # Désactiver le signal PWM pour chaque servo

finally:
    pca.deinit()  # Nettoyer le PCA9685 pour libérer les ressources