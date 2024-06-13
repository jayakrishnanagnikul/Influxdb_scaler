import numpy as np
import time
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Parameters
bucket = "DB-test"
org = "Agnikul"
token = "t5LCW4sEaXgaNjqAwMAgaNyUImD0yeInR1sscmUbPGfb5d_F4r5kvRk1lNu7pkNzxA7kldwyB59PFFlPVafvHw=="
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

# Generate time values
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate sine wave values
sine_wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)

# Generate sine wave data

# t = np.arange(0, duration, sampling_interval)
# sine_wave = np.sin(2 * np.pi * frequency * t)

print("sine dta generated with size ",len(t))

# Write data to InfluxDB
for i in range(len(t)):
    point = Point("sine_wave").tag("device", "sensor1").field("value", sine_wave[i]).time(time.time_ns(), WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
    time.sleep(0.1)

print("data written in DB")
# Query data from InfluxDB
query = f'from(bucket: "{bucket}") |> range(start: -{duration + 1}s) |> filter(fn: (r) => r._measurement == "sine_wave")'
result = query_api.query(org=org, query=query)
# Extract data
times = []
values = []
for table in result:
    for record in table.records:
        times.append(record.get_time())
        values.append(record.get_value())

# Plot data
plt.figure(figsize=(10, 6))
plt.plot(t, sine_wave)
plt.title('INPUT Sine Wave')
plt.show()
plt.plot(times, values)
plt.title('Sine Wave')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
