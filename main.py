from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

@app.get("/")
def hello():
    return {"message": "Just the start"}

@app.get('/about')
def about():
    return {"message": "I am maybe an engineer, dont know i will survive or not"}