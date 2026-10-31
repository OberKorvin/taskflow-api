from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow Database Server")


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)


@app.post("/tasks", status_code=201, response_model=schemas.TaskResponse)
def create_task(task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_new_task(db, task_data)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_single_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, updated_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    return crud.update_existing_task(db, task, updated_data)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    crud.delete_existing_task(db, task)
    return {"message": f"Задача #{task_id} успешно удалена!"}


@app.get("/tasks/filter/status", response_model=list[schemas.TaskResponse])
def filter_by_status(completed: bool, db: Session = Depends(get_db)):
    return crud.filter_tasks_by_status(db, completed)


@app.get("/tasks/search/title", response_model=list[schemas.TaskResponse])
def search_tasks(keyword: str, db: Session = Depends(get_db)):
    return crud.search_tasks_by_keyword(db, keyword)


@app.get("/tasks/stats/count")
def get_tasks_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)