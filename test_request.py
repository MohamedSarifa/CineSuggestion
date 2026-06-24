import requests

url = "https://www.omdbapi.com/?apikey=7c140df&t=Interstellar"

response = requests.get(url)

print(response.status_code)
print(response.text)