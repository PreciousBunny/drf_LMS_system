FROM python:3.11-slim-bullseye
WORKDIR /app
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/

CMD ./manage.py migrate

# Команда для запуска приложения при старте контейнера
# CMD ["python", "manage.py", "runserver"]
