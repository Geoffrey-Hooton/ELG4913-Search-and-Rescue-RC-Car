#Thermal Cam DAQ

import pithermalcam as ptc
import csv
import time
import board
import busio

#Need to initialize the camera connected to the i2c bus
i2c_bus = busio.I2C(board.SCL,board.SDA,frequency=800000)
mlx = ptc.pi_therm_cam.adafruit_mlx90640.MLX90640(i2c_bus)

def write_csv(data, filename = 'avg_temp.csv'):
    with open(filename, mode = 'a', newline = '') as file:
        myWriter = csv.writer(file)
        myWriter.writewrow(data)

write_csv(["Date & Time", "Avg temp C", "Message"])
#The camera frame is a 32x24 matrix, so we initialize to 768=32x24
frame = [0]*768
while True:

    #Calculating the avg temp in a frame
    mlx.getFrame(frame)
    avg_temp_C = sum(frame)/len(frame)
    message = 'N/A'
    if avg_temp_C > 30 and avg_temp_C<50:
        print("There may be a human there.")
        message = "There may be a human there."
    elif avg_temp_C >200:
        print("Don't go further. There may be a fire up ahead.")
        message = "Don't go further. There may be a fire up ahead."
    date_time = time.strftime('%Y-%m-%d %H:%M:%S')

    app_row = [date_time, avg_temp_C, message]
    write_csv(app_row)
    #Get data every 5 seconds
    time.sleep(5)




