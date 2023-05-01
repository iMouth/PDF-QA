FROM python:3.9.16

WORKDIR /backend

RUN python3 -m pip install --upgrade pip

COPY . .

RUN ./requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

ENV FASTCHAT_BASEURL http://FastChat:8030

CMD [ "python3", "manage.py", "runserver", "backend:8000" ]

