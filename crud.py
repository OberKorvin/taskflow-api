from sqlalchemy.orm import Session
import models
import schemas


# 1. Получить все задачи
def get_all_tasks(db: Session):
    return db.query(models.TaskDB).order_by(models.TaskDB.id.desc()).all()


# 2. Получить одну задачу по ID (вспомогательная функция для поиска, обновления и удаления)
def get_task_by_id(db: Session, task_id: int):
    return db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()


# 3. Создать задачу
def create_new_task(db: Session, task_data: schemas.TaskCreate):
    new_task = models.TaskDB(title=task_data.title, completed=task_data.completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# 4. Обновить задачу
def update_existing_task(db: Session, task: models.TaskDB, updated_data: schemas.TaskCreate):
    task.title = updated_data.title
    task.completed = updated_data.completed
    db.commit()
    db.refresh(task)
    return task


# 5. Удалить задачу
def delete_existing_task(db: Session, task: models.TaskDB):
    db.delete(task)
    db.commit()


# 6. Фильтровать задачи по статусу (выполнена/не выполнена)
def filter_by_status(completed: bool, db: Session):
    return db.query(models.TaskDB).filter(models.TaskDB.completed == completed).all()


# 7. Поиск задач по слову в названии
def search_tasks_by_keyword(db: Session, keyword: str):
    return db.query(models.TaskDB).filter(models.TaskDB.title.contains(keyword)).all()


# 8. Статистика задач
def get_stats(db: Session):
    total = db.query(models.TaskDB).count()
    completed = db.query(models.TaskDB).filter(models.TaskDB.completed == True).count()
    pending = total - completed
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }