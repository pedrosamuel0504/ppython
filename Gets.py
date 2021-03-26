from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Depends,HTTPException,Request
from sqlalchemy.orm import Session
import crud,Models,DBO
from dbs import SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

gets = APIRouter()

gets.mount("/static",StaticFiles(directory=".",html=True))
templates = Jinja2Templates(directory="." )

head = ('<!DOCTYPE html><html><head><meta charset="ISO-8859-1"><link rel="stylesheet" href="css_js/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"><title>Clients</title></head>')
body = ('<body><h3>Clients</h3><button><a href="http://localhost:8000/form">New Client</a></button><button><a href = "http://localhost:8000" align = "right" >Atras</a></button><table border="1"><tr><td>Email</td><td>Item</td><td> </td></tr>')
body1_0 = ('<body><h3>Clients</h3> <button><a href = "http://localhost:8000/users/" align = "right" >Atras</a></button>  <table border="1"><tr><td>ID</td><td>Email</td><td>Status</td><td>Delete</td></tr>')
bodyItem = ('<body><h3>Clients</h3><button><a href="http://localhost:8000/form">Edit</a></button>  <button><a href = "http://localhost:8000/users/" align = "right" >Atras</a></button>  <table border="1"><tr><td>ID</td><td>Title</td><td>Description</td></tr>')
body2 = ('</table></body></html>')

#Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()



############ DEFAULT HOME INDEX #######################
@gets.get("/")
def home(request:Request):
  return templates.TemplateResponse("index.html",{"request":request})

############ CREATE USERS ###########################

@gets.get("/form", response_class=HTMLResponse)
def form_get():
    return '''<form action="http://localhost:8000/users/" method="post"> 
    Email:<input type="text" name="email" value=""/> <br></br>
    Password:<input type="text" name="password" value=""/> <br></br>
    <input type="submit"/> <br></br>
    </form>'''



############## CREATE ITEMS #############################

@gets.get("/users/itemEdit/{item_id}",response_class=HTMLResponse)
def updateItemGet(item_id:int , db:Session = Depends(get_db)):
  Item = crud.get_item(db= db , ID= item_id)
  print(Item)
  return f'''<form action="http://localhost:8000/users/itemEdit/{(str)(item_id)}" method="post"> 
    New Title:      <input type="text" name="title" value=""/> <br></br>
    New Description:<input type= "text" name="description" value=""/> <br></br>
    <input type="submit"/> <br></br>
    </form>'''



############# EDIT USERS #############################

@gets.get("/edit/{user_id}",response_class=HTMLResponse)
def userEdit(user_id:int , db:Session = Depends(get_db)):
  User = crud.get_user(db= db , user_id= user_id)
  return '''<form action="http://localhost:8000/usersEdit/'''+(str)(user_id)+'''" method="post"> 
    Old Email:    <input type="text" name="old_email" value = '''+User.email+'''/> <br></br>
    New Email:<input type="text" name="email" value="Insert your new email"/> <br></br>
    <input type="submit"/> <br></br>
    </form>'''



############# EDIT ITEMS ###################################

@gets.get("/users/{user_id}/items/", response_class= HTMLResponse)
def CreateItemGet(user_id:int):
  return f'''<form action="/users/{user_id}/items/" method="post"> 
    Title:<input type="text" name="title" value=""/> <br></br>
    Description:<input type="text" name="description" value=""/> <br></br>
    <input type="hidden" name="owner_id" value = {user_id} /> <br></br>
    <input type="submit"/> <br></br>
    </form>'''



############# GET USERS #####################################

@gets.get("/users/",response_class= HTMLResponse)
def see_user( db: Session = Depends(get_db)):
  global head,body,body2
  User = crud.get_users(db= db)
  return head+body+User+body2



########### GET USER ITEM ####################################

@gets.get("/users/items/{user_id}",response_class=HTMLResponse)
def seeParticularItem(user_id:int , db:Session = Depends(get_db)):
  print('USER ID::',user_id)
  return crud.get_user_items(db= db , user_id= user_id)



############ GET SPECIFIC USER ###############################

@gets.get("/users/{user_id}" , response_class= HTMLResponse)
def getUser(user_id:int ,db: Session = Depends(get_db) ):
  status = "inactive"
  db_user = crud.get_user(db, user_id=user_id)
  db_Item = crud.get_item(db= db , ID= user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  if db_user.is_active:
    status = "active"
  return head+body1_0+(f'<button><a href="http://localhost:8000/edit/{user_id}">Edit</a></button>' )+(f"<td> {db_user.id} </td><td>{db_user.email}</td><td>{status}</td><td><button><a href = 'http://localhost:8000/delete/"+(str)(user_id)+"'> Delete </button></td>")+body2


############# GET SPECIFIC ITEM ###############################

@gets.get("/items/{item_id}")
def seeItems(item_id:int , db: Session = Depends(get_db)):
  db_Item = crud.get_item(db= db , ID= item_id)
  return head+body1_0+(f"<td> {db_Item.id} </td> --- <td> {db_Item.title} </td> --- <td>{db_Item.description}</td>")+body2





########### DELETE USER #######################################

@gets.get("/delete/{user_id}",response_class=HTMLResponse)
def delete(user_id:int , db:Session = Depends(get_db)):
  User = crud.get_user(db= db , user_id= user_id)
  crud.delete_user(db= db , user_id= user_id)
  return "<html><body><h1>You successfull deleted User : "+User.email+"</h1> <br></br> <button><a href = 'http://localhost:8000/users/'>Atras</button></body></html>"



############ DELETE ITEM ######################################

@gets.get("/item/delete/{item_id}",response_class=HTMLResponse)
def ItemDelete(item_id:int , db:Session = Depends(get_db)):
  crud.delete_item(db= db , item_id= item_id)
  return "<html><body><h1>You successfull deleted Item</h1> <br></br> <button><a href = 'http://localhost:8000/users/'>Atras</button></body></html>"



