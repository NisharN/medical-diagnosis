#pydantic gives perfect data schema  from passing from backend to frontend in structured format

from pydantic import BaseModel

class SignUpRequest(BaseModel):
    username:str
    password:str
    role:str
    
