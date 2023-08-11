
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