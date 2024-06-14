import requests
import datetime

# Parameters
url = "http://localhost:8086/api/v2/delete"
token = "sOUQsISLh_NrZMiDLYOrd9tnhgD-GRppfuQus1WQfbsW_FOMVUIm_c-2o428MOySuUyLZixLkSwl6jWUA_9b_Q=="  # Replace with your API token
org = "Agnikul"      # Replace with your organization name
bucket = "test_bucket"  # Replace with your bucket name
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}
current_time = datetime.datetime.utcnow().isoformat() + "Z"
data = {
    "start": "1970-01-01T00:00:00Z",
    "stop": current_time,  # Replace with the end time or use "now()"
    "predicate": "_measurement=\"sine_wave\""
}

# Send delete request
response = requests.post(url, headers=headers, json=data, params={"org": org, "bucket": bucket})

if response.status_code == 204:
    print("Data deleted successfully.")
else:
    print(f"Failed to delete data: {response.status_code}")
    print(response.text)
