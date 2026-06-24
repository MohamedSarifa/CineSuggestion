import requests

response = requests.get(
    "https://www.google.com",
    timeout=20
)

print(response.status_code)