FROM python:3.11-slim

<<<<<<< HEAD
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
=======
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Bot database will be written to /data (mounted as PVC)
WORKDIR /data
CMD ["python", "/app/main.py"]
>>>>>>> 32d949b61c9114294bd92e46752659634f8a7903
