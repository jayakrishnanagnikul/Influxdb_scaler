import numpy as np
import time
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# Parameters
bucket = "test_bucket"
org = "Agnikul"
token = "sOUQsISLh_NrZMiDLYOrd9tnhgD-GRppfuQus1WQfbsW_FOMVUIm_c-2o428MOySuUyLZixLkSwl6jWUA_9b_Q=="
url = "http://localhost:8086"

# Create an InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

amplitude = 1      # Amplitude of the sine wave
frequency = 1      # Frequency in Hz
phase = 0          # Phase in radians
sampling_rate = 1000  # Sampling rate in samples per second
duration = 2       # Duration in seconds

sine_wave_data=[]

start_time = time.time_ns()

for i in range(0,2000):

    current_time = start_time + i * int(1.0 / sampling_rate * 1e9)  # 0.1 seconds in nanoseconds
    sine_value = amplitude * np.sin(2 * np.pi * frequency * current_time * 1e-9 + phase)
    sine_value2 = amplitude * np.sin(2 * np.pi * frequency * current_time * 1e-9 + 10)
    sine_value3 = amplitude * np.sin(2 * np.pi * frequency * current_time * 1e-9 + 3)


    
    point = (
        Point("sine_wave")
        .tag("device", "sensor")
        .field("value", sine_value)
        .time(current_time , WritePrecision.NS))
    
    point2=(Point("sine_wave")
        .tag("device", "sensor2")
        .field("value", sine_value2)
        .time(current_time , WritePrecision.NS))
    
    point3=(Point("sine_wave")
        .tag("device", "sensor3")
        .field("value", sine_value3)
        .time(current_time , WritePrecision.NS))

    write_api.write(bucket=bucket, org=org, record=[point,point2,point3])
    print("entered data",i,end="\r")
    # time.sleep(1.0 / sampling_rate)
    # print("\r")
