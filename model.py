from pydantic import BaseModel

class Users(BaseModel):
    id:int
    username:str
    password:str
    role:str

class Product(BaseModel):
    product_id:int
    quantity:int

