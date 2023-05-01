#!/bin/bash

python3 -m fastchat.serve.controller --host FastChat --port 21001 &

export CUDA_VISIBLE_DEVICES=1,2,3

python3 -m fastchat.serve.model_worker \
        --host FastChat \
        --worker-address "http://FastChat:21002" \
        --controller-address "http://FastChat:21001" \
        --model-name 'vicuna-13b-v1.1' \
        --model-path models/vicuna-13b \
        --num-gpus 3 &

python3 -m fastchat.serve.api --host FastChat --port 8030
