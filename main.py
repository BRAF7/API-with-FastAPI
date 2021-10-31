#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI 
#Allows to know that a parameter its body type
from fastapi import Body

app = FastAPI()

#Models
class Person(BaseModel):
    first_name : str
    last_name : str
    #Optional parameters
    #Expect String
    #Default None
    married : Optional[str] = None    

@app.get('/')
def home() -> str:
    return 'Hola desde FastAPI'

@app.post('/person/new')
def create_person(person : Person = Body(...)) -> str:

    return '200 OK'