from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

from sqlalchemy.orm import relationship


class CategoriesTableSchema(Base):

    __tablename__ ='categories'
    category_Id=Column(Integer,primary_key=True,index=True)
    created_on=Column(DateTime)
    name=Column(String)
    users=relationship('User',back_populates='owner')
    user_id=Column(Integer,ForeignKey('User.user_id'))
    cate=relationship('Ledger', back_populates='led')

class Account(Base):
    
    __tablename__='Account'
    account_id=Column(Integer,primary_key=True, index= True)
    account_name=Column(String)
    initial_balance=Column(Integer)
    type=Column(String)
    created_at=Column(DateTime)
    uses=relationship('User',back_populates='account')
    user_id=Column(Integer,ForeignKey('User.user_id'))
    use=relationship('Ledger', back_populates='ledger')
    


class Ledger(Base):
    
    __tablename__='Ledger'
    
    ledger_id=Column(Integer,primary_key=True, index= True)
    amount=Column(Integer)
    account_id=Column(Integer, ForeignKey('Account.account_id'))
    category_Id=Column(Integer, ForeignKey('categories.category_Id'))
    transaction=Column(String)
    user_id= Column(Integer, ForeignKey('User.user_id'))
    transfer_to=Column(String)
    created_at=Column(DateTime)
    ledger=relationship('Account', back_populates='use') 
    led=relationship('CategoriesTableSchema',back_populates='cate')
    lead=relationship('User', back_populates='urs')                                                                                                                                                                                                       
    
    
class User(Base):
    
    __tablename__='User'
    
    user_id=Column(Integer,primary_key=True, index= True)
    name=Column(String)
    email=Column(String)
    created_at=Column(DateTime)
    owner=relationship('CategoriesTableSchema', back_populates='users')
    account=relationship('Account', back_populates='uses')
    urs=relationship('Ledger', back_populates='lead')  
    


