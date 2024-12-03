import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Configurer I2C
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)

# Régler la fréquence PWM pour les servos
pca.frequency = 50  # Fréquence standard pour les servomoteurs (50Hz)

# Choisir les canaux PWM pour les 4 servos en rotation et le 5ᵉ servo
rotation_servos = [pca.channels[0], pca.channels[1], pca.channels[2], pca.channels[3]]
lift_servo = pca.channels[4]  # Servo pour soulever/abaisser l'objet

# Fonction pour définir l'angle d'un servo
def set_servo_angle(channel, angle):
    pulse_width = int((angle / 180.0) * 1000 + 1000)  # Conversion de l'angle en largeur d'impulsion
    pwm_value = int((pulse_width / 20000) * 65535)  # Conversion en 16 bits
    channel.duty_cycle = pwm_value  # Régler le cycle de service PWM

# Fonction pour arrêter un servo
def stop_servo(channel):
    channel.duty_cycle = 0  # Mettre le cycle de service à zéro pour désactiver le signal

# Fonction pour faire tourner les 4 servos dans le même sens
def rotate_servos_same_direction_4(rotation_servos):
    for angle in range(0, 181, 10):  # Faire varier l'angle de 0 à 180° avec un pas de 10°
        print(f"Déplacement de tous les servos à {angle} degrés")
        for i, channel in enumerate(rotation_servos):
            print(f"  -> Servo {i+1} à {angle} degrés")
            set_servo_angle(channel, angle)  # Appliquer l'angle à chaque servo
        time.sleep(0.5)  # Pause pour voir le mouvement
    print("Rotation complète pour 4 servos")

# Fonction pour faire descendre et remonter un objet avec le 5ᵉ servo
def move_lift_servo(lift_servo, down_angle, up_angle, repeat=3):
    for _ in range(repeat):
        print(f"Descente du lift servo à {down_angle} degrés")
        set_servo_angle(lift_servo, down_angle)  # Abaisser l'objet
        time.sleep(1)  # Pause pour simuler la descente
        print(f"Remontée du lift servo à {up_angle} degrés")
        set_servo_angle(lift_servo, up_angle)  # Remonter l'objet
        time.sleep(1)  # Pause pour simuler la remontée
    print("Mouvement de levage terminé")

try:
    # Faire tourner les 4 servos dans le même sens
    rotate_servos_same_direction_4(rotation_servos)

    # Faire descendre/remonter l'objet avec le 5ᵉ servo
    move_lift_servo(lift_servo, down_angle=45, up_angle=135)  # Descendre à 45°, remonter à 135°

    # Arrêter tous les servos
    print("Arrêt des servos")
    for channel in rotation_servos:
        stop_servo(channel)  # Désactiver les signaux pour les servos en rotation
    stop_servo(lift_servo)  # Désactiver le signal pour le servo de levage

finally:
    pca.deinit()  # Nettoyer le PCA9685 pour libérer les ressources
