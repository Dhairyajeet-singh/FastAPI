from fastapi import FastAPI
import uvicorn, pydantic
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import json
from fastapi import Path, Query

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