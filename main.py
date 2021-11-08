#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr
#FastAPI
from fastapi import FastAPI 
#Allows to know that a parameter its body type
from fastapi import Body, Query, Path, Form, Cookie, Header, File
from fastapi import status, UploadFile



app = FastAPI()

class HairColor(Enum):
    white = 'white'
    black = 'black'
    brown = 'brown'
    blonde = 'blonde'
    
class PersonBase(BaseModel):
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

#Models
class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        example='password'
    )




class PersonOut(PersonBase):
    pass



class Location(BaseModel):
    city: str = Field(
        ...,
        title='City',
        description='Here goes the city',
        example='Ocozocoautla'
    )
    state: str = Field(
        ...,
        title='State',
        description='Here goes the State',
        example='Chiapas'
    )
    country: str = Field(
        ...,
        title='Country',
        description='Here goes the country',
        example='Mexico'
    )




class LoginOut(BaseModel):
    username: str = Field(...,
        description='Username',
        example='admin'
    )

    message: str = Field(
        default='Login successful',
        description='Message to return to the user'
    )




@app.get(path='/', status_code=status.HTTP_200_OK)
def home() -> str:
    return 'Hola desde FastAPI'




@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
)
def create_person(
    person : Person = Body(
        ...,
        title='Create person',
        description='Creates a person. It´s required',
    )
) -> Person:
    return person

#Validations: Query Parameters


@app.get(path='/person/detail', status_code=status.HTTP_200_OK)
def show_person(
    name : Optional[str] = Query(
        default=None,
        minlength=1, 
        maxlength=50,
        title='Person name',
        description='This is the person name. It´s between 1 and 50 characters',
        example='Mar'
        ),
    #Not recommended to use required with Query parameters
    age : int = Query(
        ...,
        title='Person age',
        description='This is the person age. It´s required',
        example=15,
        ),
) -> dict:
    return {name : age}



#Path paramters
@app.get(path='/person/detail/{person_id}', status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=1,
    )
) -> dict:
    return {person_id : 'It exists'}



#Validations: Request Body 
@app.put(path='/person/{person_id}', status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is the person ID',
        #Greater than 0
        gt=0,
        example=1,
    ),
    person : Person = Body(...),
    location : Location = Body(...)
) -> dict:
    result = person.dict()
    result.update(location.dict())
    return result




@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
)
def login(
    username: str = Form(
        ...,
        min_length=3,
        max_length=10,
        example='root'
    ),

    password: str = Form(
        ...,
        min_length=8,
        max_length=50,
        example='toor'
    ),
) -> LoginOut: return LoginOut(username=username)




@app.post(path='/contact', status_code=status.HTTP_200_OK)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Mar'
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Pascasio'
    ),
    email: EmailStr = Form(
        ...,
        example='mar@gmail.com'
    ),
    message: str = Form(
        ...,
        min_length=20,
        max_length=280,
        example='Esta es una linea de codigo con más de 20 caracteres'
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
) -> str: return user_agent




@app.post(path='/post-image',status_code=status.HTTP_200_OK)
def post_image(
    image: UploadFile = File(...)
): return {
    #getting the name of the file
    'filename': image.filename,
    #show the type of image
    'format': image.content_type,
    #convert bytes to kb
    'size(kb)': round(len(image.file.read()) / 1024, 2)
}