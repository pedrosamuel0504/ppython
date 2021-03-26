import uvicorn
# 910127 from passlib.context import CryptContext
from fastapi import FastAPI,BackgroundTasks
from Gets import gets
from Posts import posts

app = FastAPI() 

###### INCLUDE BACKGRAOUND PROCESS

app.include_router(gets)
app.include_router(posts)


###### RUN THE PROCCESS 

if __name__ == "__main__":
  uvicorn.run("main:app",reload= True)
