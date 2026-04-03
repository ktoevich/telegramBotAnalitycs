FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем локальные файлы проекта в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной исходный код (исключая то, что в .dockerignore)
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "main.py"]
