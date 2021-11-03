#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr
#FastAPI
from fastapi import FastAPI 
#Allows to know that a parameter its body type
from fastapi import Body, Query, Path



app = FastAPI()

class HairColor(Enum):
    white = 'white'
    black = 'black'
    brown = 'brown'
    blonde = 'blonde'

#Models
class Person(BaseModel):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Mar'
    )
    last_name : str = Field(
        ...,
        min_length=1, 
        max_length= 50,
        #----------------------------------------------------------------
        #We´re adding a parameter example 
        # ---------------------------------------------------------------
        example='Pascacio'
    )
    #Optional parameters
    #Expect String
    #Default None
    married : Optional[bool] = Field(default=None, example=True)
    hair_color : Optional[HairColor] = Field(default='black')
    email : EmailStr = Field(
        ...,
        title='Person email',
        description='Here goes the email',
        example='mar@gmail.com'
    )




class Location(BaseModel):
    city: str
    state: str
    country: str




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



#Validations: Request Body 
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is the person ID',
        #Greater than 0
        gt=0
    ),
    person : Person = Body(...),
    location : Location = Body(...)
) -> dict:
    result = person.dict()
    result.update(location.dict())
    return result