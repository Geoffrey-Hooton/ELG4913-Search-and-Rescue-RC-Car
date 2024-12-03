import pygame
import math
from math import floor
from adafruit_rplidar import RPLidar

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

# Function to map lidar data to screen coordinates
def polar_to_cartesian(angle, distance):
    if distance > MAX_DISTANCE:
        distance = MAX_DISTANCE
    angle_rad = math.radians(angle)
    x = CENTER_X + int(distance * math.cos(angle_rad) * (WIDTH / 2) / MAX_DISTANCE)
    y = CENTER_Y + int(distance * math.sin(angle_rad) * (HEIGHT / 2) / MAX_DISTANCE)
    return x, y

# Function to draw grid and circles for reference
def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for r in range(500, WIDTH // 2, 500):
        pygame.draw.circle(screen, CIRCLE_COLOR, (CENTER_X, CENTER_Y), r, 1)
    for angle in range(0, 360, 45):
        x = CENTER_X + int((WIDTH // 2) * math.cos(math.radians(angle)))
        y = CENTER_Y + int((HEIGHT // 2) * math.sin(math.radians(angle)))
        pygame.draw.line(screen, GRID_COLOR, (CENTER_X, CENTER_Y), (x, y))

# Function to process and visualize data
def process_data():
    draw_grid()  # Clear screen and draw grid

    # Draw each scan frame in the history
    for data in scan_history:
        for angle in range(360):
            distance = data[angle]
            if distance > 0:
                x, y = polar_to_cartesian(angle, distance)
                pygame.draw.circle(screen, POINT_COLOR, (x, y), 2)

    pygame.display.flip()  # Update display

try:
    for scan in lidar.iter_scans():
        # Prepare scan data for this frame
        scan_data = [0] * 360
        for _, angle, distance in scan:
            scan_data[min([359, floor(angle)])] = distance

        # Append current frame to history and keep only last 3 frames
        scan_history.append(scan_data)
        if len(scan_history) > 3:
            scan_history.pop(0)

        # Process and visualize the recent frames
        process_data()
        clock.tick(30)  # Limit to 30 frames per second

except KeyboardInterrupt:
    print("Stopping.")
finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    pygame.quit()
