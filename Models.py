from typing import List, Optional
from fastapi import Form
from pydantic import BaseModel




class UserCreate(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(cls,email:str = Form(...) , password:str = Form(...)):
        return cls(email= email , password= password)


class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = "Havn't description"

    @classmethod
    def as_form(cls,title:str = Form(...) , description:str = Form(...)):
        return cls(title= title,description= description)

class UserEdit(BaseModel):
    email:str
    @classmethod
    def as_form(cls , email: str = Form(...)):
        return cls(email= email)

class ItemEdit(BaseModel):
    title:str
    description:str
    @classmethod
    def as_form(cls , title:str = Form(...), description:str = Form(...)):
        return cls(title= title,description= description)

