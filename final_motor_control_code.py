import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Configurer I2C
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)

# Régler la fréquence PWM pour les servos
pca.frequency = 50  # Fréquence standard pour les servomoteurs (50Hz)

# Assigner les canaux aux 4 servomoteurs pour le mouvement de la voiture
front_left_servo = pca.channels[0]
front_right_servo = pca.channels[1]
rear_left_servo = pca.channels[2]
rear_right_servo = pca.channels[3]

# Assigner le canal pour le 5ème servo (lifter)
lifter_servo = pca.channels[4]

# Fonction pour définir la vitesse ou la direction d'un servo
def set_servo_speed(channel, speed):
    """
    Définit la vitesse du servo en fonction de la valeur `speed`.
    La valeur `speed` est comprise entre -100 (reculer/baisser) et 100 (avancer/monter).
    """
    if speed == 0:  # Arrêter le servo
        channel.duty_cycle = 0
    else:
        # Convertir la vitesse (-100 à 100) en cycle de service PWM
        pulse_width = int((speed / 100.0) * 500 + 1500)  # -100 -> 1ms, 100 -> 2ms
        pwm_value = int((pulse_width / 20000) * 65535)
        channel.duty_cycle = pwm_value

# Fonction pour avancer
def move_forward():
    print("La voiture avance")
    set_servo_speed(front_left_servo, 100)
    set_servo_speed(front_right_servo, 100)
    set_servo_speed(rear_left_servo, 100)
    set_servo_speed(rear_right_servo, 100)

# Fonction pour reculer
def move_backward():
    print("La voiture recule")
    set_servo_speed(front_left_servo, -100)
    set_servo_speed(front_right_servo, -100)
    set_servo_speed(rear_left_servo, -100)
    set_servo_speed(rear_right_servo, -100)

# Fonction pour tourner à gauche (pivot)
def turn_left():
    print("La voiture tourne à gauche (pivot)")
    set_servo_speed(front_left_servo, -50)
    set_servo_speed(front_right_servo, 50)
    set_servo_speed(rear_left_servo, -50)
    set_servo_speed(rear_right_servo, 50)

# Fonction pour tourner à droite (pivot)
def turn_right():
    print("La voiture tourne à droite (pivot)")
    set_servo_speed(front_left_servo, 50)
    set_servo_speed(front_right_servo, -50)
    set_servo_speed(rear_left_servo, 50)
    set_servo_speed(rear_right_servo, -50)

# Fonction pour une courbe douce à gauche
def gentle_curve_left():
    print("La voiture tourne doucement à gauche")
    set_servo_speed(front_left_servo, 50)
    set_servo_speed(front_right_servo, 100)
    set_servo_speed(rear_left_servo, 50)
    set_servo_speed(rear_right_servo, 100)

# Fonction pour une courbe douce à droite
def gentle_curve_right():
    print("La voiture tourne doucement à droite")
    set_servo_speed(front_left_servo, 100)
    set_servo_speed(front_right_servo, 50)
    set_servo_speed(rear_left_servo, 100)
    set_servo_speed(rear_right_servo, 50)

# Fonction pour arrêter la voiture
def stop_all():
    print("La voiture s'arrête")
    set_servo_speed(front_left_servo, 0)
    set_servo_speed(front_right_servo, 0)
    set_servo_speed(rear_left_servo, 0)
    set_servo_speed(rear_right_servo, 0)

# Fonction pour lever l'objet avec le 5ème servo
def lift_object():
    print("Lever l'objet")
    set_servo_speed(lifter_servo, 100)  # Monte l'objet

# Fonction pour abaisser l'objet avec le 5ème servo
def lower_object():
    print("Abaisser l'objet")
    set_servo_speed(lifter_servo, -100)  # Abaisse l'objet

# Fonction pour arrêter le 5ème servo
def stop_lifter():
    print("Arrêter le lifter")
    set_servo_speed(lifter_servo, 0)  # Arrêter le lifter

# Séquence de test
try:
    move_forward()
    time.sleep(2)  # Avancer pendant 2 secondes

    move_backward()
    time.sleep(2)  # Reculer pendant 2 secondes

    turn_left()
    time.sleep(2)  # Tourner à gauche (pivot) pendant 2 secondes

    turn_right()
    time.sleep(2)  # Tourner à droite (pivot) pendant 2 secondes

    gentle_curve_left()
    time.sleep(2)  # Courbe douce à gauche pendant 2 secondes

    gentle_curve_right()
    time.sleep(2)  # Courbe douce à droite pendant 2 secondes

    lift_object()
    time.sleep(2)  # Lever l'objet pendant 2 secondes

    lower_object()
    time.sleep(2)  # Abaisser l'objet pendant 2 secondes

    stop_lifter()  # Arrêter le lifter
    stop_all()  # Arrêter la voiture

    print("Fin de la séquence")

finally:
    pca.deinit()  # Nettoyer le PCA9685 = fin du code