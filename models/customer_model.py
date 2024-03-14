from pydantic import BaseModel

class Customer(BaseModel):
    name : str
    role : str
    address : str
    contact : str


