import requests
response = requests.get("https://api.github.com/repos/axios/axios/commits",params = {"per_page": 100})
print(response.status_code)
data = response.json()
print(type(data))
print(len(data))
print(data[0])

