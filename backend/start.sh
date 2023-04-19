#!/bin/bash

python3 -m manage runserver 0.0.0.0:8000 &

python3 -m fastchat.serve.controller --host backend --port 21001 &

python3 -m fastchat.serve.model_worker --host backend --worker-address "http://backend:21002" --controller-address "http://backend:21002" --model-name 'vicuna-7b-v1.1' --model-path backend/pdfparser/models/vicuna-7b/ &

python3 -m fastchat.serve.api --host backend --port 8030