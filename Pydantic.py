from pydantic import BaseModel, EmailStr, Field
from typing import List,Dict, Optional, Annotated

class patient(BaseModel):

    name: Annotated[str,Field(max_lenght=50, min_length=3, description="Name of the patient", example="John Doe")]

    age: int 
    email: EmailStr
    weight: float = Field(gt=0, lt=120)
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    contact_details: Dict[str,str]

def insert_patient(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("patient inserted")

def update_patient(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("patient updated")

patient_info = {'name': 'john','age':20, 'email': 'bhelu@gmail.com', 'weight': 75.4, 'contact_details': {'phone': '1234567890'}}
patient1 = patient(**patient_info)
insert_patient(patient1)
