from fastapi import FastAPI
import uvicorn, pydantic
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import json

app = FastAPI()
@app.get('/')
def msg():
    return {"message": "Patients information management system"}

@app.get('/about')
def about():
    return {"message": "This system provides api to manage information about patients."}

def load_data():
    try:
        with open('patients.json','r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return 0
    except json.JSONDecodeError:
        return 0

@app.get('/patients')

def view():
    data = load_data()
    if data == 0:
        raise HTTPException(status_code=404, detail="No data found")
    return data


