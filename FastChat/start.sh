#!/bin/bash

python3 -m fastchat.serve.controller --host FastChat --port 21001 &

python3 -m fastchat.serve.model_worker --host FastChat --worker-address "http://FastChat:21002" --controller-address "http://FastChat:21001" --model-name 'vicuna-7b-v1.1' --model-path models/vicuna-7b/ &

python3 -m fastchat.serve.api --host localhost --port 8030