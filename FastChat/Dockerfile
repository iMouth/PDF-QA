FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /FastChat

RUN apt-get update

RUN apt-get install -y python3-pip

COPY . .

RUN python3 -m pip install --upgrade pip

RUN pip3 install -e .

ENV FASTCHAT_CONTROLLER_URL http://localhost:8030

EXPOSE 8030

RUN chmod 777 start.sh

CMD [ "bash", "start.sh" ]