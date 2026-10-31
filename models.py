from database import Base
from sqlalchemy import Boolean, Column, Integer, String

#  5. МОДЕЛЬ ТАБЛИЦЫ (Чертеж того, как задачи хранятся в базе на жестком диске)
class TaskDB(Base):
    __tablename__ = "tasks"  # Название таблицы внутри базы данных

    # Описываем 3 колонки таблицы (ровно как ключи в нашем старом словаре!):
    # primary_key=True означает, что база САМА будет выдавать уникальные номера 1, 2, 3...
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)