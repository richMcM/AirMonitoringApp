import logging
import datetime
import serial
# ttyUSB0 is the device for the first USB serial convertor
device='/dev/ttyUSB0'

def read_nova_pm_sensor():
    # creating an instance of the sensor specifying the serial port and baudrate
    SDS_PMsensor = serial.Serial(device, 9600)

    if not SDS_PMsensor.isOpen():
        SDS_PMsensor.open()

    # Read 10 bytes from the serial port
    msg = SDS_PMsensor.read(10)
    
    assert msg[0] == ord(b'\xaa')
    assert msg[1] == ord(b'\xc0')
    assert msg[9] == ord(b'\xab')
    #Calculating Readings
    pm25 = (msg[3] * 256 + msg[2]) / 10.0
    pm10 = (msg[5] * 256 + msg[4]) / 10.0
    
    # Using checksum to check for errors in the data
    checksum = sum(v for v in msg[2:8]) % 256
    assert checksum == msg[8]
    # Getting current data and time for readings
    date = datetime.datetime.today()
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    
    return {'Date': date,'PM10': pm10, 'PM2_5': pm25}

'''
# Can be used to write Sensor Data to a CSV file
def append_csv(filename, field_names, row_dict):
    """
    Create or append row of data to csv file.
    """
    file_exists = os.path.isfile(filename)
    with io.open(filename, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile,
                                delimiter=',',
                                lineterminator='\n',
                                fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)
'''
LOG_FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'