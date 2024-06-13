import numpy as np
import time
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Parameters
bucket = "your_bucket"
org = "your_org"
token = "your_token"
url = "http://localhost:8086"
frequency = 10  # 10 Hz
duration = 5  # seconds
sampling_interval = 1 / frequency

# Create an InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# Generate sine wave data
t = np.arange(0, duration, sampling_interval)
sine_wave = np.sin(2 * np.pi * frequency * t)

# Write data to InfluxDB
for i in range(len(t)):
    point = Point("sine_wave").tag("device", "sensor1").field("value", sine_wave[i]).time(time.time_ns(), WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
    time.sleep(sampling_interval)

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
plt.plot(times, values)
plt.title('Sine Wave')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
