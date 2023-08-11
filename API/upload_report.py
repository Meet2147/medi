from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector
import io

app = FastAPI()

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "medilink",
}

# SQLAlchemy model for reports
Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"
    
    report_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer)
    report_name = Column(String)
    report_date = Column(Date)
    report_location = Column(String)
    report_file = Column(String)  # Store the file location or path

# Database setup
DATABASE_URL = "mysql+mysqlconnector://your_username:your_password@localhost/your_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# API endpoint to upload a report
@app.post("/upload-report/")
def upload_report(patient_id: int, report_name: str, report_date: str, report_location: str, report: UploadFile = File(...)):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO reports (patient_id, report_name, report_date, report_location, report_file)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = (
        patient_id,
        report_name,
        report_date,
        report_location,
        report.filename,
    )

    cursor.execute(insert_query, data)
    connection.commit()

    # Save the uploaded file to a suitable location (e.g., "uploads" folder)
    file_path = f"uploads/{report.filename}"
    with open(file_path, "wb") as f:
        f.write(report.file.read())

    cursor.close()
    connection.close()

    return JSONResponse(content={"message": "Report uploaded successfully"})

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
