from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .models import SignUpRequest
from .hash_utils import hash_password, verify_password
from ..config.db import users_collection

#tags are mainly used for grouping the routes in swagger ui
router=APIRouter(prefix='/auth',tags=['auth'])
security=HTTPBasic()

def authenticate(credentials:HTTPBasicCredentials=Depends(security)):
    user=users_collection.find_one({"username":credentials.username})
    if not user or not verify_password(credentials.password,user['password']):
        raise HTTPException(status_code=401,details='Invalid credentials')
    return {'username':user["username"],'role':user['role']}


@router.post("/signup")
def signup(request:SignUpRequest):
    #check if user already exists
    if users_collection.find_one({"username":request.username}):
        raise HTTPException(status_code=400,detail="Username already exists")
    users_collection.insert_one({
       "username":request.username,
       "password":hash_password(request.password),
       "role":request.role

    })
    return {"message":"User Created Successfully"}

@router.get("/login")
def login(user=Depends(authenticate)):
    return{"username":user['username'],"role":user['role']}
    
