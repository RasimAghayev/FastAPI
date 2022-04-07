from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class PackageIn(BaseModel):
    secret_id: int
    name: str
    number: str
    description: Optional[str]=None

class Package(BaseModel):
    name: str
    number: str
    description: Optional[str]=None

app=FastAPI()

@app.get('/')
async def hello_world():
    return  {"Hello":"World"}

@app.post("/package",response_model=Package,response_model_include={"description"})
async def make_package(package: PackageIn):
    return package

# @app.post("/package/{priority}")
# async def make_package(priority: int,package: Package, value: bool):
#     return {"priority": priority, **package.dict(), "value":value }

# @app.get("/component/{componenet_id}") #path parameter
# async def get_component(componenet_id):
#     return {"comonenet_id":componenet_id}

# @app.get("/component/")
# async def read_component(number:int, text:Optional[str]): #query parametr
#     return {"number":number,"text":text}
