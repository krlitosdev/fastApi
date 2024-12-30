from typing import Union
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

#Conexion a la base de datos
import sqlalchemy as db 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DEFINE THE DATABASE CREDENTIALS
user = 'admin'
password = 'admin'
host = '127.0.0.1'
port = 3306
database = 'FastApi'

import pyodbc
print(pyodbc.drivers())
print('--------------------------------------------')

engine = db.create_engine("mysql+pyodbc://{0}:{1}@{2}:{3}/{4}?driver=ODBC+Driver+17+for+SQL+Server".format(
            user, password, host, port, database
        ), echo=True) 


#def get_connection():
#    return create_engine(
#        url="mysql+pyodbc://{0}:{1}@{2}:{3}/{4}".format(
#            user, password, host, port, database
#        ),echo=True
#    )

#try:
#        # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
#        engine = get_connection()
#        print(f"===> Connection to the {host} for user {user} created successfully.")
#except Exception as ex:
#        print("===? Connection could not be made due to the following error: \n", ex)


# Configurar el logger
logging.basicConfig(
    level=logging.INFO,  # Nivel de logs: DEBUG, INFO, WARNING, ERROR, CRITICAL
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)




app = FastAPI()
scheduler = BackgroundScheduler()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar tarea periódica
def periodic_task():
    logger.info("Ejecutando Tarea en segundo plano")
    print("Tarea ejecutada!")
    
scheduler.add_job(periodic_task, IntervalTrigger(seconds=10))
scheduler.start()

@app.on_event("startup")
def on_startup():
    logger.info("Iniciando la App")

@app.get("/api")
async def read_root():
    print("---> Ejecutando Pedidos")
    logger.info("Se ha llamado al endpoint raíz")
    return {"Hello": "World"}
