from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Адрес нашей базы данных:
# Говорим создать файл tasks.db прямо в текущей папке проекта
DATABASE_URL = "sqlite:///./tasks.db"

# 2. Создаем "Движок" (engine) — это мост между Python и файлом базы данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Фабрика сессий — через "сессию" мы будем открывать соединение, 
# сохранять задачи и закрывать соединение
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Базовый класс для создания таблиц
Base = declarative_base()


# 5. МОДЕЛЬ ТАБЛИЦЫ (Чертеж того, как задачи хранятся в базе на жестком диске)
class TaskDB(Base):
    __tablename__ = "tasks"  # Название таблицы внутри базы данных

    # Описываем 3 колонки таблицы (ровно как ключи в нашем старом словаре!):
    # primary_key=True означает, что база САМА будет выдавать уникальные номера 1, 2, 3...
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)


# 6. Команда: "Если файла tasks.db и таблицы tasks еще нет — создай их прямо сейчас!"
Base.metadata.create_all(bind=engine)