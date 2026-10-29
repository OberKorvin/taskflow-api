from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # <-- ДОБАВЬ ЭТУ СТРОЧКУ

# Создаем сам сервер
app = FastAPI(title="TaskFlow Server")

# Твоя база задач (уже знакомый тебе список словарей!)
all_tasks = [
    {"id": 1, "title": "Купить чай", "completed": True},
    {"id": 2, "title": "Написать первый код", "completed": False},
    {"id": 3, "title": "Проверить терминал", "completed": False},
    {"id": 4, "title": "Jod", "completed": False}
]


# МАРШРУТ 1: Когда кто-то заходит по ссылке /tasks, отдаем весь список
@app.get("/tasks")
def get_tasks():
    return all_tasks


# МАРШРУТ 2: Поиск одной задачи по её номеру (например: /tasks/2)
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):  # : int говорит серверу, что номер должен быть целым числом
    for task in all_tasks:
        if task["id"] == task_id:
            return task
            
    raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")

# 1. ПРАВИЛА ВХОДА (Схема данных Pydantic):
# Говорим серверу: новая задача обязана содержать текстовое поле title,
# а поле completed по умолчанию будет False (не выполнено)
class TaskCreate(BaseModel):
    title: str
    completed: bool = False


# 2. МАРШРУТ СОЗДАНИЯ ЗАДАЧИ (Метод POST)
@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    # Считаем порядковый номер для новой задачи (сколько сейчас задач + 1)
    new_id = len(all_tasks) + 1
    
    # Собираем новую карточку задачи (словарь) из того, что прислал пользователь
    task_dict = {
        "id": new_id,
        "title": new_task.title,
        "completed": new_task.completed
    }
    
    # Команда .append() кладет новую карточку в конец нашего списка all_tasks
    all_tasks.append(task_dict)
    
    # Возвращаем созданную карточку обратно пользователю как подтверждение
    return task_dict

# МАРШРУТ 4: Отметить задачу выполненной (Метод PUT — Обновление)
@app.put("/tasks/{task_id}")
def complete_task(task_id: int):
    # Ищем задачу по номеру в нашем списке
    for task in all_tasks:
        if task["id"] == task_id:
            task["completed"] = True  # Меняем статус на Выполнено!
            return task               # Возвращаем обновленную карточку
            
    raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")


# МАРШРУТ 5: Удалить задачу по номеру (Метод DELETE — Удаление)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in all_tasks:
        if task["id"] == task_id:
            all_tasks.remove(task)    # Команда .remove() удаляет задачу из списка
            return {"message": f"Задача #{task_id} успешно удалена!"}
            
    raise HTTPException(status_code=404, detail="Задача с таким ID не найдена")

# МАРШРУТ 6: Фильтр задач по статусу (выполнено / не выполнено)
@app.get("/tasks/filter/status")
def filter_tasks(completed: bool):
    result = []  # Создаем пустую коробку-список для подходящих задач
    
    for task in all_tasks:
        if task["completed"] == completed:
            result.append(task)
          # 👇 ТВОЯ ЗАДАЧА ЗДЕСЬ:
            # Напиши условие if: если поле task["completed"] равно переменной completed,
            # то добавь эту задачу в список result с помощью команды: result.append(task)

    return result