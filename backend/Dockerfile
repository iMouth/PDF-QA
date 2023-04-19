FROM python:3.9.16

WORKDIR /backend

RUN python3 -m pip install --upgrade pip

COPY . .

RUN ./requirements.txt

RUN pip3 install -e backend/pdfparser/FastChat/

EXPOSE 8000

EXPOSE 8030

ENV PYTHONUNBUFFERED 1

ENV FASTCHAT_BASEURL http://backend:8030

ENV FASTCHAT_CONTROLLER_URL http://backend:8030

RUN chmod 777 start.sh

CMD [ "bash", "start.sh" ]
