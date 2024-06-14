import numpy as np
import time
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

global time_values
global sine_values
time_values=[]
sine_values=[]

def sine_with_time():
    global time_values
    global sine_values


# Initialize a list to store the sine wave data
    sine_wave_data = []

    # Get the start time
    start_time = time.time()

    # Run the loop for the specified duration
    while time.time() - start_time < duration:
        # Get the current time
        current_time = time.time()

        # Calculate the sine wave value
        sine_value = amplitude * np.sin(2 * np.pi * frequency * current_time + phase)

        # Store the time and sine value in the list
        sine_wave_data.append((current_time, sine_value))

        # Sleep for the appropriate amount of time to maintain the sampling rate
        time.sleep(1.0 / sampling_rate)

    # Convert the data to a numpy array for further processing or analysis
    sine_wave_data = np.array(sine_wave_data)

    # Print the generated data
    # print(sine_wave_data)
    
    time_values = sine_wave_data[:, 0]
    sine_values = sine_wave_data[:, 1]

# Parameters
bucket = "test_bucket"
org = "Agnikul"
token = "sOUQsISLh_NrZMiDLYOrd9tnhgD-GRppfuQus1WQfbsW_FOMVUIm_c-2o428MOySuUyLZixLkSwl6jWUA_9b_Q=="
url = "http://localhost:8086"

# Create an InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# Define parameters
amplitude = 1      # Amplitude of the sine wave
frequency = 1      # Frequency in Hz
phase = 0          # Phase in radians
sampling_rate = 1000  # Sampling rate in samples per second
duration = 2       # Duration in seconds

sine_with_time()

print("sine data generated with size ",len(time_values))

# Write data to InfluxDB
for i in range(len(time_values)):
    point = Point("sine_wave").tag("device", "sensor1").field("value", sine_values[i]).time(time.time_ns(), WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
    print(".\r",end=" \r")
    time.sleep(0.1)

print("data written in DB")
# Query data from InfluxDB
query = f'from(bucket: "{bucket}") |> range(start: -{len(time_values) + 1}s) |> filter(fn: (r) => r._measurement == "sine_wave")'
result = query_api.query(org=org, query=query)
# Extract data
db_times = []
db_values = []
for table in result:
    for record in table.records:
        db_times.append(record.get_time())
        db_values.append(record.get_value())

# Plot data
plt.figure(figsize=(10, 6))
plt.plot(time_values, sine_values,color="red",label="generated_sinewave")
plt.legend(loc='upper left')
plt.twiny()
plt.plot(db_times, db_values,color="blue",label="retrived_data_sinewave")
plt.title('INPUT Sine Wave')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()