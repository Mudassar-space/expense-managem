from passlib.context import CryptContext


pwd_cxt= CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash:
    def bcrypt(password:str):
        hashedpassword=pwd_cxt.hash(password)
        return hashedpassword