from pydantic import BaseModel

class Users(BaseModel):
    id:int
    username:str
    password:str
    role:str


'''
        "id": 1,
        "username": "admin",
        "password": "$5$rounds=535000$p46Uwmn27BOGzUN0$EEyAE3o.HOMPVekajXRX2tuPPMT7xhs55V.jsumSmI8",
        "role": "admin"
'''