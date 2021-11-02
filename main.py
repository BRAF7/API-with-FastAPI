#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI 
#Allows to know that a parameter its body type
from fastapi import Body, Query, Path



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
def create_person(
    person : Person = Body(
        ...,
        title='Create person',
        description='Creates a person. It´s required'
        )
) -> str:
    return '200 OK'

#Validations: Query Parameters


@app.get('/person/detail')
def show_person(
    name : Optional[str] = Query(
        default=None,
        minlength=1, 
        maxlength=50,
        title='Person name',
        description='This is the person name. It´s between 1 and 50 characters'
        ),
    #Not recommended to use required with Query parameters
    age : int = Query(
        ...,
        title='Person age',
        description='This is the person age. It´s required',
        ),
) -> dict:
    return {name : age}



#Path paramters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
    )
) -> dict:
    return {person_id : 'It exists'}
