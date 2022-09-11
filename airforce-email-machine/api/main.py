from fastapi import FastAPI
from pydantic import BaseModel
from .crawler import getAirmans, selectAirman
from .sender import send

app = FastAPI()

class Airman(BaseModel):
    url : str

class Email(BaseModel):
    relationship : str
    title : str
    contents : str
    password : str
    
class Sender(BaseModel):
    name : str
    address : str
    addressDetail : str

@app.get("/airmans/")
async def airmans(name: str, birthDate: str):
    airmans = getAirmans(name, birthDate)
    return airmans

@app.get("/airmans/{airmanIndex}")
async def airman(airmanIndex: int, name: str, birthDate: str):
    airmans = getAirmans(name, birthDate)
    airman = selectAirman(airmans, airmanIndex)
    return airman

@app.post("/send/")
async def sendEmail(airman: Airman, sender: Sender, email: Email):
    success = send(airman, sender, email)
    return success
    
