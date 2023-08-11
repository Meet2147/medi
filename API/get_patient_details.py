from fastapi import FastAPI
import mysql.connector

app = FastAPI()

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "medilink",
}

# API endpoint to get patient details with linked reports
@app.get("/patient/{patient_id}")
def get_patient_details(patient_id: int):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    select_patient_query = "SELECT * FROM patients WHERE patient_id = %s"
    cursor.execute(select_patient_query, (patient_id,))
    patient = cursor.fetchone()

    if patient is None:
        cursor.close()
        connection.close()
        return {"message": "Patient not found"}

    select_reports_query = "SELECT * FROM reports WHERE patient_id = %s"
    cursor.execute(select_reports_query, (patient_id,))
    reports = cursor.fetchall()

    cursor.close()
    connection.close()

    patient_details = {"patient": patient, "reports": reports}
    return patient_details

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
