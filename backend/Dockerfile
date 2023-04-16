FROM python:3.9.16-alpine3.17

WORKDIR /backend

RUN python3 -m pip install --upgrade pip

COPY requirements.txt .

RUN ./requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
