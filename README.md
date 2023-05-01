# PDF-QA

## How to Run

1. Install [Docker](https://www.docker.com/) based on your operating system.
1. If you have Nvidia GPUs follow the instructions to download [nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-container-toolkit) and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker).

---

### Method 1: With NVIDIA GPUS

Visit [FastChat](https://github.com/lm-sys/FastChat) and follow their instructions to get the vicuna model. Also read their documentation on CPU and GPU requirements. 

Place the model somewhere in the *FastChat* directory and update the --model-path in *FastChat/start.sh*.

Run the following command to see your Nvidia GPU information:

```bash
nvidia-smi
```

Using this information change the CUDA_VISIBLE_DEVICES in *FastChat/start.sh* and update --num-gpus accordingly. 

Run the following command in the root directory to start up the services:

```bash
docker-compose up
```

*NOTE: This will take some time the first time running this*

Visit localhost:3000 to use PDF-QA.

---

### Method 2: Without NVIDIA GPUS:

Visit [FastChat](https://github.com/lm-sys/FastChat) and follow their instructions to get the vicuna model. Also read their documentation on CPU and GPU requirements. 

Place the model somewhere in the *FastChat* directory and update the --model-path in *FastChat/start.sh*.

Change --device to cpu (or mps if you are on mac) in *FastChat/start.sh*.

Comment out or remove everything under deploy for both fastchat and grobid in *docker-compose.yaml* services.

Run the following command in the root directory to start up the services:

```bash
docker-compose up
```

*NOTE: This will take some time the first time running this*

Visit localhost:3000 to use PDF-QA.

---

### Method 3: With CHATGPT

If you do not meet the GPU or CPU requirements and a ChatGPT api key you can do the following: 

Comment out or remove the fastchat service in *docker-compose.yaml*

Make a .env file in *backend* directory with your API KEY in the following format:

```bash
CHATGPT_API_KEY=PLACE_KEY_HERE
```

Run the following command in the root directory to start up the services:

```bash
docker-compose up
```

Visit localhost:3000 to use PDF-QA.

