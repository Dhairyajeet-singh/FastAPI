from fastapi import FastAPI
import uvicorn, pydantic
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import json
from fastapi import Path, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal


app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., max_length=10, min_length=3, description="Patient ID", example="P001")]
    name: Annotated[str, Field(..., max_length=50, min_length=3, description="Name of the patient", example="John Doe")]
    age: Annotated[int, Field(..., gt=0, lt=150, description="Age of the patient", example=30)]
    city: Annotated[str, Field(..., max_length=50, description="City of the patient", example="New York")]
    gender: Annotated[Literal['male','female','other'], Field(..., max_length=10, description = 'Your Gender (male, female, other)')]
    height: Annotated[float, Field(..., gt=0, lt=300, description="Height of the patient in cm", example=175.5)]
    weight: Annotated[float, Field(..., gt=0, lt=250, description="Weight of the patient in kg", example=70.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        height_in_m = self.height / 100  # Convert height from cm to m
        bmi = round((self.weight/ (height_in_m**2)), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
    
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

def save_data(data):
    with open('patients.json', 'w') as file:
        json.dump(data, file)
@app.get('/patients')

def view():
    data = load_data()
    if data == 0:
        raise HTTPException(status_code=404, detail="No data found")
    return data

@app.get('/patients/{id}')
def view_by_id(id: str = Path(..., description="Enter patient number to view details"), example = "P001"):
    data = load_data()
    if id in data:
        return data[id]
    raise HTTPException(status_code = 404, detail = "patient not found, enter valid patient number")

@app.get('/sort')
def sort_patient(sort_by: str = Query(...,description="Enter the field to sort by", example="name"), order:str = Query('asc', description='sort in asc or desc order')):
    valid_fileds = ['name','age','weight']
    if sort_by not in valid_fileds:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fileds)}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")
    
    data = load_data()
    if data == 0:
        raise HTTPException(status_code=404, detail="No data found")
    
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by,0), reverse = sort_order)
    return sorted_data


@app.post('/create')
def create_patients(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})
