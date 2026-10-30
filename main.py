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


# 1. ПОЛУЧИТЬ ВСЕ ЗАДАЧИ (Новые сверху!)
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    # .order_by(TaskDB.id.desc()) сортирует задачи от самой новой к самой старой
    tasks = db.query(TaskDB).order_by(TaskDB.id.desc()).all()
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


# 4. ПОЛНОЕ ОБНОВЛЕНИЕ ЗАДАЧИ (PUT — меняем и название, и статус)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_data: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")
    
    # Обновляем оба поля тем, что прислал пользователь:
    task.title = updated_data.title
    task.completed = updated_data.completed
    
    db.commit()          # Сохраняем изменения в файл tasks.db
    db.refresh(task)     # Обновляем карточку
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

# 6. ФИЛЬТР ПО СТАТУСУ ЧЕРЕЗ БАЗУ ДАННЫХ (GET)
@app.get("/tasks/filter/status")
def filter_by_status(completed: bool, db: Session = Depends(get_db)):
    # База сама отбирает только те строки, где колонка completed совпадает с запросом
    tasks = db.query(TaskDB).filter(TaskDB.completed == completed).all()
    return tasks


# 7. ПОИСК ЗАДАЧ ПО СЛОВУ В НАЗВАНИИ (GET)
@app.get("/tasks/search/title")
def search_tasks(keyword: str, db: Session = Depends(get_db)):
    # Команда .contains(keyword) ищет задачи, внутри названия которых есть нужное слово
    tasks = db.query(TaskDB).filter(TaskDB.title.contains(keyword)).all()
    return tasks

# 8. СТАТИСТИКА ЗАДАЧ (GET)
@app.get("/tasks/stats/count")
def get_tasks_stats(db: Session = Depends(get_db)):
    total = db.query(TaskDB).count()
    completed = db.query(TaskDB).filter(TaskDB.completed == True).count()
    pending = db.query(TaskDB).filter(TaskDB.completed == False).count()  
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }