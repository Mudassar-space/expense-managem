from typing import Optional
from unicodedata import category
from pydantic import BaseModel, EmailStr
from datetime import datetime

# from sqlalchemy import DateTime

# format = "%Y-%m-%dT%H:%M:%S.%fZ"

class Categories(BaseModel):
    
    name: str
    created_on: datetime
    user_id: int
    
    
class Cate_response_model(BaseModel) :
    
    created_on: datetime
    name: str
    category_Id: int
 
    
class Cate_update_response(BaseModel):
    created_on: datetime
    name: str
  
       
class User(BaseModel):
    
    name: str
    # last_name: str
    email: str #Optional [EmailStr]
    created_at: datetime


class User_response(BaseModel):
    
    name: str
    email: str
    user_id: int
    created_at: str 
    

class Account(BaseModel):
    user_id: int
    account_name: str
    initial_balance: int
    type: str
    created_at: datetime
    
    
class Account_response(BaseModel):
    user_id:int 
    account_id: int
    initial_balance: int
    created_at: datetime
    type: str
    account_name: str
    

class Responses(BaseModel):
    
    status: bool
    message: str
    

class Ledger(BaseModel):
    
    amount: int
    account_id: int
    category_Id: int
    user_id: int
    transaction: str
    transfer_to: str
    created_at: datetime
    

    
    