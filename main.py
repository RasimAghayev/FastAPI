from fastapi import FastAPI
from typing import Optional

app=FastAPI()

@app.get('/')
async def hello_world():
    return  {"Hello":"World"}

@app.get("/component/{componenet_id}")
async def get_component(componenet_id):
    return {"comonenet_id":componenet_id}

@app.get("/component/")
async def read_component(number:int, text:str):
    return {"number":number,"text":text}

