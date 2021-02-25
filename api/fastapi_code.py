import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home1():
    return {"Hello": "Pedro1"}
    
@app.get("/first/{id}")
def first(id: int):
    return {"Hello": id}    

if __name__ == "__main__":
    uvicorn.run("fastapi_code:app",reload=True)