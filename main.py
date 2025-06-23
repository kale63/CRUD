from fastapi import FastAPI
from pydantic import BaseModel
import csv

app = FastAPI()

# Modelo con nombre "Alumnos"
class Alumnos(BaseModel):
    Matricula: str
    Nombre: str
    Edad: int
    Genero: str
    Carrera: str
    Semestre: int
    Trabajo: str
    Estado: str
    Hobby: str
    Preferencia: str

# Lista de usuarios (solo los primeros 40 registros del CSV)
classmates_list = []

with open('COPIA_bdmodelos.csv', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        if i >= 39:
            break  

        classmate = Alumnos(
            Matricula=row["Matricula"],
            Nombre=row["Nombre"],
            Edad=int(row["Edad"]),
            Genero=row["Genero"],
            Carrera=row["Carrera"],
            Semestre=int(row["Semestre"]),
            Trabajo=row["Trabajo"],
            Estado=row["Estado"],
            Hobby=row["Hobby"],
            Preferencia=row["Preferencia"]
        )
        classmates_list.append(classmate)


# GET todos los alumnos
@app.get("/alumnos/")
async def get_users():
    return classmates_list

# POST para agregar nuevo alumno
@app.post("/alumnos/")
async def alumnos(classmate: Alumnos):
    for saved_classmate in classmates_list:
        if saved_classmate.Matricula == classmate.Matricula:
            return {"error": "El alumno ya existe"}
    classmates_list.append(classmate)
    return classmate

# PUT para modificar a un alumno existente
@app.put("/alumnos/")
async def alumnos(classmate: Alumnos):
    found = False
    for index, saved_classmate in enumerate(classmates_list):
        if saved_classmate.Matricula == classmate.Matricula:
            classmates_list[index] = classmate
            found = True
    if not found:
        return {"error": "No se ha actualizado al alumno"}
    else:
        return classmate

# DELETE eliminar a un alumno por Matricula
@app.delete("/alumnos/")
async def alumnos(matricula: str):
    found = False
    for index, saved_classmate in enumerate(classmates_list):
        if saved_classmate.Matricula == matricula:
            del classmates_list[index]
            found = True
            return {"message": "Alumno eliminado correctamente"}
    if not found:
        return {"error": "No se ha encontrado el alumno para eliminar"}

# uvicorn main:app --reload 