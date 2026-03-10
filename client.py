import requests

url = "http://127.0.0.1:5000/login"
data1 = {"username":"admin","password":'1234'}

response = requests.post(url,json=data1)

print('status',response.status_code)
print('response',response.json())