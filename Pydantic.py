from pydantic import BaseModel
from typing import List,Dict, Optional

class patient(BaseModel):

    name: str 
    age: int 
    weight: float
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    contact_details: Dict[str,str]

def insert_patient(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("patient inserted")

def insert_patient(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("patient updated")

patient_info = {'name': 'john','age':20, 'weight': 75.4}
patient1 = patient(**patient_info)
insert_patient(patient1)
