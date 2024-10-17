FROM python:3.9-slim

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY .env /code/.env
RUN pip install -r requirements.txt

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем исходный код в контейнер
COPY . /app

# Запускаем приложение
CMD python bot.py