FROM python:3.11.0-slim-buster

LABEL maintainer ="artem.kharchenko.job@gmail.com"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]