import requests
import json
from flask import jsonify

#LOGIN
url = "http://127.0.0.1:5000/user/login"
data1 = {"username":"luffy","password":"1234"}
response = requests.post(url,json=data1)

data = response.json()

if 'token'not in data:
    print(data)
    exit()
else:
    token = data['token']
    print('status',response.status_code)
    print('response',response.json())

# #VIEW PRODUCTS
# url = "http://127.0.0.1:5000/product"
#
# headers = {'Authorization':f'Bearer {token}'}
#
# response = requests.get(url,headers=headers)
#
# print('status',response.status_code)
# print('response',response.json())

# #SIGNUP
# url = "http://127.0.0.1:5000/user/signup"
# data_signup = {"username":"brook","password":"1234","role":"admin"}
# send_token = {'Authorization':f'Bearer {token}'}
# response = requests.post(url,json=data_signup,headers=send_token)
# print('status',response.status_code)
# print('response',response.text)

#VIEW USERS
url = "http://127.0.0.1:5000/user/view"
send_token = {'Authorization': f'Bearer {token}'}
response = requests.get(url,headers=send_token)
print('status',response.status_code)
print('response',response.text)

# #DELETE
# url = "http://127.0.0.1:5000/user/delete"
# delete_data = {"id": 6}
# send_token = {'Authorization':f'Bearer {token}'}
# response = requests.post(url,json=delete_data,headers=send_token)
# print(response.status_code)
# print(response.json())
