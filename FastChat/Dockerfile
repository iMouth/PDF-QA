
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

WORKDIR /FastChat

RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3-pip


ENV FASTCHAT_CONTROLLER_URL http://FastChat:8030

ENV FASTCHAT_BASEURL http://FastChat:8030

EXPOSE 8030

EXPOSE 21001

EXPOSE 21002



