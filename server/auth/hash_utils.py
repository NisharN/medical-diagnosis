import bcrypt

#taking password as str and return string
#gensalt is used for generating hash with random salt
def hash_password(password:str)-> str:
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")


def verify_password(password:str,hashed:str)->bool:
    return bcrypt.checkpw(password.encode("utf-8"),hashed.encode("utf-8"))