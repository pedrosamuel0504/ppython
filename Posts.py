from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
import crud,Models,DBO
from dbs import SessionLocal
posts = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


########### EDIT USERS #######################

@posts.post("/usersEdit/{user_id}",response_class=HTMLResponse)
def update(user_id:int , user:Models.UserEdit = Depends(Models.UserEdit.as_form) , db:Session = Depends(get_db)):
  crud.editUser(db= db , userEdit= user , user_id= user_id) 
  return "<html><body><h1>You User was edited successfully <br></br></h1> <br></br> <button><a href = 'http://localhost:8000/users/'>Atras</button></body></html>"
  
########### EDIT ITEMS ########################

@posts.post("/users/itemEdit/{item_id}",response_class=HTMLResponse)
def updateItemPost(item_id:int , item:Models.ItemEdit = Depends(Models.ItemEdit.as_form) , db:Session = Depends(get_db)):
  crud.editItem(db= db , itemEdit= item , item_id= item_id)
  return "<html><body><h1>You Item was edited successfully <br></br></h1> <br></br> <button><a href = 'http://localhost:8000/users/'>Atras</button></body></html>"


############ CREATE USERS ######################

@posts.post("/users/",response_class=HTMLResponse)
def create_user(user:Models.UserCreate = Depends(Models.UserCreate.as_form) , db: Session = Depends(get_db)):
  db_user = crud.get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  crud.create_user(db=db, user=user)
  return "<html><body><h1>You User was created successfully <br></br></h1> <br></br> <button><a href = 'http://localhost:8000/users/'>Atras</button></body></html>"


############# CREATE ITEMS ######################

@posts.post("/users/{user_id}/items/",response_class=HTMLResponse)
def create_user_item(user_id:int ,item: Models.ItemCreate = Depends(Models.ItemCreate.as_form), db: Session = Depends(get_db)):
  Item = crud.create_user_item(db= db , item= item , user_id= user_id)
  User = crud.get_user(db= db , user_id= user_id)
  return "<html><body><h1>You successfull create Item  </h1> <br></br> <button><a href = 'http://localhost:8000/users/'>Atras</button></body></html>"

