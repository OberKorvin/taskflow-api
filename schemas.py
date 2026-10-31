from pydantic import BaseModel


# Схема для создания и обновления задачи (то, что присылает клиент)
class TaskCreate(BaseModel):
    title: str
    completed: bool = False


# Схема для ответа сервера (добавляется id из базы данных)
class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True