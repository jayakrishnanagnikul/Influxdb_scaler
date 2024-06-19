import numpy as np
import time
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


start_time = time.time_ns()
temp=[]
point_list=[]
data_start_time=time.time()
print(data_start_time)
#iterates over all sensors
for sen_no in range(1,10):
    point=[]
    time_list=[]
    sine_wave_data=[]
    
    #creates whole sensor values 
    for i in range(0,2000):
        time_data = start_time + i * int(1.0 / sampling_rate * 1e9)  # 0.1 seconds in nanoseconds
        input_data = amplitude *sen_no/100* np.sin(2 * np.pi * frequency * time_data * 1e-9 + phase)
        
        sine_wave_data.append(input_data)
        time_list.append(time_data)
  
        sensor_point= (
            Point("sine_wave")
            .tag("device", "sensor"f'{sen_no}')
            .field("value", sine_wave_data[i])
            .time(time_list[i] , WritePrecision.NS))
        
        point.append(sensor_point)
        time.sleep(1.0 / sampling_rate)
    point_list.append(point)
    print("generated data for sensor ",sen_no,end="\r")

print("data generation completed",time.time())

start_write=time.time()
write_api.write(bucket=bucket, org=org, record=point_list)
end_write=time.time()
print("data writing completed diff is ",end_write-start_write)
print("start_write",start_write,"end_write",end_write)