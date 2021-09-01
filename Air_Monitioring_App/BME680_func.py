import time
import board
from busio import I2C
import adafruit_bme680

import os
import csv
import io

import logging
import datetime

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)


def read_bme680_sensor(device=bme680):
    
    date = datetime.datetime.today()
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    temp = device.temperature
    gas = device.gas
    humidity = device.relative_humidity
    
    
    
    return {'Date': date, 'Temp': temp, 'Gas': gas, 'Humidity': humidity}


# Can be used to write Sensor Data to a CSV file
def append_csv(filename, field_names, row_dict):
    
    #Create or append row of data to csv file.
    
    file_exists = os.path.isfile(filename)
    with io.open(filename, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile,
                                delimiter=',',
                                lineterminator='\n',
                                fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)


LOG_FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s' # Format for the log file
