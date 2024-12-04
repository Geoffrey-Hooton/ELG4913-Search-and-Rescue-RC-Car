#Geophone DAQ

import time
import Adafruit_ADS1x15
import numpy as np
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
import csv

#Initializing the ADC (ADS1115)
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
GAIN = 16

#----------------------------------------------------
#----------------------------------------------------

#Function to collect the data 
def data_collect():

    data =[]
    start_time = time.time()

    #Sampling 20 seconds of data at a time
    #The time different between each data point is 0.01s
    #This way, we know that each point is at x0=0, x1=0.01, x2 = 0.02...
    while (time.time() - start_time) < 20:
        data.append(adc.read_adc_difference(0, gain=GAIN))
        time.sleep(0.02)
    return data

#----------------------------------------------------
#----------------------------------------------------

#Function is to detect a heartbeat in the dataset acquired from data_collect()
def heart_detect(data):

    fft_values = fft(data)
    freqs = fftfreq(len(data), d=0.02)

    pos_freqs = freqs[:len(data)//2]
    mags = np.abs(fft_values[:len(data)//2])

    main_index = np.argmax(mags)
    main_freq = pos_freqs[main_index]

    # If the magnitude is significant enough
    if mags[main_index] > np.mean(mags) * 3:
        return main_freq
    
    return main_freq

#----------------------------------------------------
#----------------------------------------------------

#This will be the main part of the code

#Writing a csv file with the detected periodic signal frequencies
filename = "HeartDetect.csv"
with open(filename, mode='w', newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date","Time","Message", "Frequency (Hz)"])
#Looping forever until the program is stopped

while True:
    print("Sampling data for 20 seconds.")
    data = data_collect()

    heartbeat_frequency = heart_detect(data)
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        date = time.strftime("%Y-%m-%d")
        timestamp = time.strftime("%H:%M:%S")
        if heartbeat_frequency>0:
            message = "Potential Heartbeat Detected"
            print(message)
            writer.writerow([date,timestamp,message, f"{heartbeat_frequency:.2f}"])
        else:
            message = "Nothing Detected"
            print(message)
            writer.writerow([date,timestamp,message,"None"])
    
    #After sampling for 20 seconds, we sleep for 30
    time.sleep(30)