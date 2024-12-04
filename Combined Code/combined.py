import multiprocessing
import sys

# Function to run the thermal camera
def run_thermalcam():
    import pithermalcam as ptc
    import time

    while True:
        try:
            ptc.display_camera_live()
        except Exception as e:
            print(f"Thermal Camera Error {e}")

# Function to run the lidar visualization
def run_fast_lidar():
    import pygame
    import math
    from math import floor
    from adafruit_rplidar import RPLidar

    PORT_NAME = "/dev/ttyUSB0"
    lidar = RPLidar(None, PORT_NAME, timeout=3)
    WIDTH, HEIGHT = 800, 800
    CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    MAX_DISTANCE = 4000

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lidar Visualization")
    clock = pygame.time.Clock()

    BACKGROUND_COLOR = (20, 20, 30)
    POINT_COLOR = (255, 215, 0)
    GRID_COLOR = (50, 50, 70)
    CIRCLE_COLOR = (100, 100, 150)

    scan_history = []

    def polar_to_cartesian(angle, distance):
        if distance > MAX_DISTANCE:
            distance = MAX_DISTANCE
        angle_rad = math.radians(angle)
        x = CENTER_X + int(distance * math.cos(angle_rad) * (WIDTH / 2) / MAX_DISTANCE)
        y = CENTER_Y + int(distance * math.sin(angle_rad) * (HEIGHT / 2) / MAX_DISTANCE)
        return x, y

    def draw_grid():
        screen.fill(BACKGROUND_COLOR)
        for r in range(500, WIDTH // 2, 500):
            pygame.draw.circle(screen, CIRCLE_COLOR, (CENTER_X, CENTER_Y), r, 1)
        for angle in range(0, 360, 45):
            x = CENTER_X + int((WIDTH // 2) * math.cos(math.radians(angle)))
            y = CENTER_Y + int((HEIGHT // 2) * math.sin(math.radians(angle)))
            pygame.draw.line(screen, GRID_COLOR, (CENTER_X, CENTER_Y), (x, y))

    def process_data():
        draw_grid()
        for data in scan_history:
            for angle in range(360):
                distance = data[angle]
                if distance > 0:
                    x, y = polar_to_cartesian(angle, distance)
                    pygame.draw.circle(screen, POINT_COLOR, (x, y), 2)
        pygame.display.flip()

    try:
        for scan in lidar.iter_scans():
            scan_data = [0] * 360
            for _, angle, distance in scan:
                scan_data[min([359, floor(angle)])] = distance

            scan_history.append(scan_data)
            if len(scan_history) > 3:
                scan_history.pop(0)

            process_data()
            clock.tick(30)

    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        pygame.quit()

# Function to run motor control UI
def run_motor_ui():
    from PyQt5.QtWidgets import QApplication
    from motor_ui import MotorControlUI
    app = QApplication(sys.argv)
    window = MotorControlUI()
    window.show()
    sys.exit(app.exec_())

# Function to run geophone graph
def run_differential_graph_display():
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import Adafruit_ADS1x15

    adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    GAIN = 16
    x_len = 500
    y_range = [-750, 750]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = list(range(0, x_len))
    ys = [0] * x_len
    ax.set_ylim(y_range)
    line, = ax.plot(xs, ys)
    plt.title('Geophone Data')
    plt.xlabel('Data Points (Approximately 25 Readings each Second)')
    plt.ylabel('Voltage Value Post Gain Adjustment')

    def animate(i, ys):
        value = adc.read_adc_difference(0, gain=GAIN)
        ys.append(value)
        ys = ys[-x_len:]
        line.set_ydata(ys)
        return line,

    ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=1, blit=True)
    plt.show()

# Main process to manage all sensors
if __name__ == "__main__":
    processes = [
        multiprocessing.Process(target=run_thermalcam),
        multiprocessing.Process(target=run_fast_lidar),
        multiprocessing.Process(target=run_motor_ui),
        multiprocessing.Process(target=run_differential_graph_display),
    ]

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()
