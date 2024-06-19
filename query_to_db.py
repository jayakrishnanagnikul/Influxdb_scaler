from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import matplotlib.pyplot as plt

bucket = "test_bucket"
org = "Agnikul"
token = "sOUQsISLh_NrZMiDLYOrd9tnhgD-GRppfuQus1WQfbsW_FOMVUIm_c-2o428MOySuUyLZixLkSwl6jWUA_9b_Q=="

url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()
# Query data from InfluxDB
query = f'from(bucket: "{bucket}") 
        |> range(start: -10h) 
        |> filter(fn: (r) => r._measurement == "sine_wave" and r.device == "sensor1")'
result = query_api.query(org=org, query=query)
print(result)
# Extract data
db_times = []
db_values = []
for table in result:
    for record in table.records:
        db_times.append(record.get_time())
        db_values.append(record.get_value())

# Plot data
plt.figure(figsize=(10, 6))
plt.legend(loc='upper left')
plt.plot(db_times, db_values,color="blue",label="retrived_data_sinewave")
plt.title('INPUT Sine Wave')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()