import requests
import json
from flask import jsonify

#LOGIN
url = "http://127.0.0.1:5000/user/login"
data1 = {"username":"admin","password":"12345"}
response = requests.post(url,json=data1)

data = response.json()

if 'token'not in data:
    print(data)
    exit()
else:
    token = data['token']
    print('status',response.status_code)
    print('response',response.text)

#SIGNUP
url = "http://127.0.0.1:5000/user/signup"
data_signup = {"username":"franky","password":"1234","role":"user"}
send_token = {'Authorization':f'Bearer {token}'}
response = requests.post(url,json=data_signup,headers=send_token)
print('status',response.status_code)
print('response',response.json())

# #VIEW
# url = "http://127.0.0.1:5000/product"
#
# headers = {'Authorization':f'Bearer {token}'}
#
# response = requests.get(url,headers=headers)
#
# print('status',response.status_code)
# print('response',response.json())