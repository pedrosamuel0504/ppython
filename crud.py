from sqlalchemy.orm import Session
from typing import List
import DBO , Models ,dbs

head = ('<!DOCTYPE html><html><head><meta charset="ISO-8859-1"><link rel="stylesheet" href="css_js/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"><title>Clients</title></head>')
bodyGUI = ('<body><h3>Clients</h3><button><a href = "http://localhost:8000/users/" align = "right" >Atras</a></button><table border="1"><tr><td>ID</td><td>Title</td><td>Description</td><td>Delete</td><td>Edit</td></tr>')#Get User from DB
body2 = ('</table></body></html>')
adedit = ('')


############ ---- GET FUNCTIONS -----################


def get_user(db: Session , user_id: int):
  return db.query(DBO.User).filter(DBO.User.id == user_id).first()

def get_user_by_email(db:Session , email:str):
  return db.query(DBO.User).filter(DBO.User.email == email).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
  return db.query(DBO.Item.title,DBO.Item.description).offset(skip).limit(limit).all()

def get_item(db:Session , ID:int):
  return db.query(DBO.Item).filter(DBO.Item.id == ID).first()



def get_users(db:Session ):
  a = ""
  status = "Inactive"
  for ID,email in db.query(DBO.User.id,DBO.User.email).all():
    item = db.query(DBO.Item.title).filter(DBO.Item.owner_id == ID).all()
    print(item)
    if ID and email :
      print(f"ID:{ID} -- Email:{email}")
      a = a + ("<p>")
      a = a + ("<tr><td> <a href = 'http://localhost:8000/users/"+(str)(ID)+"'> "+ email +"</a></td> ")
    if item:
      print('ID:: ',ID)
      a = a + ("<td><button><a href= 'http://localhost:8000/users/items/"+(str)(ID)+"'>ITEM</a></button></td>")
    if not item:
      a = a + ("<td><button><a href= 'http://localhost:8000/users/"+(str)(ID)+"/items/'>CREATE</a></button></td>")

      a = a + ("</tr></p>")
  return a


def get_user_items(db: Session, user_id:int):
  global head,bodyGUI,body2,gui
  a = " "
  for title, description , ID in db.query(DBO.Item.title,DBO.Item.description,DBO.Item.id).filter(DBO.Item.owner_id == user_id).all():
    print("Title:"+title+" --- Description:"+description+" -- ID:"+(str)(ID))
    if title and description:
      a = a + ("<p>")
      a = a + ("<tr> <td>"+(str)(ID)+"</td> <td> "+ title +"</td> <td> "+description+"</td> ")
      a = a + ("<td><button><a href ='http://localhost:8000/item/delete/"+(str)(ID)+"'> Delete </button></td><td><button><a href = 'http://localhost:8000/users/itemEdit/"+(str)(ID)+"'>Edit</button></td>")
      a = a + ("</tr></p>")
  
  return head+bodyGUI+("<button><a href = 'http://localhost:8000/users/"+(str)(user_id)+"/items/' align = 'right' >Add</a> </button>")+a+body2


########################## ---- CREATE FUNCTIONS ------#################################


def create_user(db: Session, user: Models.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = DBO.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def create_user_item(db: Session, item: Models.ItemCreate, user_id: int):
    db_item = DBO.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

################## --- EDITS FUNCTIONS ----#################################

def editUser(db:Session, userEdit:Models.UserEdit ,user_id:int):
  User = db.query(DBO.User).get(user_id)
  User.email = userEdit.email
  db.commit()
  db.refresh(User)
  return User

def editItem(db:Session , itemEdit:Models.ItemEdit , item_id:int):
  print('item id:',item_id)
  Item = db.query(DBO.Item).get(item_id)
  print('Item:',Item)
  Item.title = itemEdit.title
  Item.description = itemEdit.description
  db.commit()
  db.refresh(Item)
  return Item


################### ----- DELTE FUNCTIONS -----############################################
def delete_user(db : Session , user_id:int):
  user = db.query(DBO.User).get(user_id)
  db.delete(user)
  db.commit()

def delete_item(db:Session , item_id:int):
  item = db.query(DBO.Item).get(item_id)
  db.delete(item)
  db.commit()

