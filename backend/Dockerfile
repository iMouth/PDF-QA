FROM python:3.9.16

WORKDIR /backend

COPY . .

RUN python3 -m pip install --upgrade pip

RUN ./requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

ENV FASTCHAT_BASEURL http://localhost:8030

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

