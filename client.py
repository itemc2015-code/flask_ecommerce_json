import requests
import json

#LOGIN
url = "http://127.0.0.1:5000/login"
data1 = {"username":"luffy","password":"1234","role":"admin"}
response = requests.post(url,json=data1)

data = response.json()
if 'token'not in data:
    print(data)
else:
    token = data['token']
    print('status',response.status_code)
    print('response',response.json())

#SIGNUP
url = "http://127.0.0.1:5000/signup"
data_signup = {"username":"franky","password":"1234","role":"user"}
response = requests.post(url,json=data_signup)
print('status',response.status_code)
print('response',response.json())

# #VIEW
# url = "http://127.0.0.1:5000"
#
# headers = {'Authorization':f'Bearer {token}'}
#
# response = requests.get(url,headers=headers)
#
# print('status',response.status_code)
# print('response',response.json())