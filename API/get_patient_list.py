from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

# Create FastAPI instance
app = FastAPI()

# Database connection setup
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "medilink"
}

# Pydantic model for input data
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    birthdate: str
    contact: str
    age: int
    address: str
    country: str

# API endpoints
@app.post("/patients/")
def create_patient(patient: PatientCreate):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO patients (first_name, last_name, birthdate, contact, age, address,country)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        patient.first_name,
        patient.last_name,
        patient.birthdate,
        patient.contact,
        patient.age,
        patient.address,
        patient.country
    )
    
    cursor.execute(insert_query, values)
    conn.commit()
    
    inserted_id = cursor.lastrowid
    
    conn.close()
    
    return {"patient_id": inserted_id}

@app.get("/patients/{patient_id}")
def read_patient(patient_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    select_query = "SELECT * FROM patients WHERE patient_id = %s"
    cursor.execute(select_query, (patient_id,))
    
    patient = cursor.fetchone()
    conn.close()
    
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient

# Similar update and delete endpoints can be implemented using MySQL queries.
# ... (previous code)

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, updated_patient: PatientCreate):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    update_query = """
        UPDATE patients
        SET first_name = %s, last_name = %s, birthdate = %s, contact = %s, age = %s, address = %s
        WHERE patient_id = %s
    """
    data = (
        updated_patient.first_name,
        updated_patient.last_name,
        updated_patient.birthdate,
        updated_patient.contact,
        updated_patient.age,
        updated_patient.address,
        patient_id,
    )

    cursor.execute(update_query, data)
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Patient updated successfully"}

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    delete_query = "DELETE FROM patients WHERE patient_id = %s"
    cursor.execute(delete_query, (patient_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Patient deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


