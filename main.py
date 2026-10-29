from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, TaskDB
from pydantic import BaseModel

app = FastAPI(title="TaskFlow Database Server")


# Вспомогательная функция: подключается к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Схема валидации (Pydantic) для создания задачи
class TaskCreate(BaseModel):
    title: str
    completed: bool = False


# 1. ПОЛУЧИТЬ ВСЕ ЗАДАЧИ (GET)
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    # Достаем из таблицы TaskDB абсолютно все строчки
    tasks = db.query(TaskDB).all()
    return tasks


# 2. СОЗДАТЬ НОВУЮ ЗАДАЧУ (POST)
@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    # Создаем объект нашей табличной модели для записи в базу
    new_task = TaskDB(title=task_data.title, completed=task_data.completed)
    
    db.add(new_task)       # Добавляем в сессию
    db.commit()            # Сохраняем на жесткий диск в tasks.db
    db.refresh(new_task)   # Обновляем объект (чтобы база вернула присвоенный ID)
    
    return new_task


# 3. ПОЛУЧИТЬ ОДНУ ЗАДАЧУ ПО ID (GET)
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    return task


# 4. ОБНОВИТЬ СТАТУС ЗАДАЧИ (PUT)
@app.put("/tasks/{task_id}")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    
    task.completed = True
    db.commit()
    db.refresh(task)
    return task


# 5. УДАЛИТЬ ЗАДАЧУ (DELETE)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    
    db.delete(task)
    db.commit()
    return {"message": f"Задача #{task_id} успешно удалена!"}