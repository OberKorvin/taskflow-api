from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Автоматически создаем таблицы в базе при старте сервера, если их еще нет
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow Database Server")


# 1. ПОЛУЧИТЬ ВСЕ ЗАДАЧИ (Новые сверху)
@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.TaskDB).order_by(models.TaskDB.id.desc()).all()


# 2. СОЗДАТЬ НОВУЮ ЗАДАЧУ
@app.post("/tasks", status_code=201, response_model=schemas.TaskResponse)
def create_task(task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.TaskDB(title=task_data.title, completed=task_data.completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# 3. ПОЛУЧИТЬ ОДНУ ЗАДАЧУ ПО ID
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_single_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    return task


# 4. ПОЛНОЕ ОБНОВЛЕНИЕ ЗАДАЧИ
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, updated_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    
    task.title = updated_data.title
    task.completed = updated_data.completed
    db.commit()
    db.refresh(task)
    return task


# 5. УДАЛИТЬ ЗАДАЧУ
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    
    db.delete(task)
    db.commit()
    return {"message": f"Задача #{task_id} успешно удалена!"}


# 6. ФИЛЬТР ПО СТАТУСУ
@app.get("/tasks/filter/status", response_model=list[schemas.TaskResponse])
def filter_by_status(completed: bool, db: Session = Depends(get_db)):
    return db.query(models.TaskDB).filter(models.TaskDB.completed == completed).all()


# 7. ПОИСК ПО СЛОВУ В НАЗВАНИИ
@app.get("/tasks/search/title", response_model=list[schemas.TaskResponse])
def search_tasks(keyword: str, db: Session = Depends(get_db)):
    return db.query(models.TaskDB).filter(models.TaskDB.title.contains(keyword)).all()


# 8. СТАТИСТИКА ЗАДАЧ
@app.get("/tasks/stats/count")
def get_tasks_stats(db: Session = Depends(get_db)):
    total = db.query(models.TaskDB).count()
    completed = db.query(models.TaskDB).filter(models.TaskDB.completed == True).count()
    pending = total - completed
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }