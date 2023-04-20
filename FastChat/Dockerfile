FROM python:3.9.16

WORKDIR /FastChat

COPY . .

RUN python3 -m pip install --upgrade pip

RUN pip3 install -e .

ENV FASTCHAT_CONTROLLER_URL http://FastChat:8030

EXPOSE 8030

EXPOSE 21001

EXPOSE 21002

RUN chmod 777 start.sh

CMD [ "bash", "start.sh" ]