# Docker environment for Tensorflow

# Contents
<!-- TOC generated with https://github.com/ekalinin/github-markdown-toc -->
<!--
 cat fls_model_standalone.md | ./gh-md-toc -
-->

* [System requirements](#System-requirements)
* [Prerequisite](#Prerequisite)
  * [For Windows Machine](#For-Windows-Machine)
  * [For Ubuntu Machine](#For-Ubuntu-Machine)
* [Install Docker](#Install-Docker)
  * [For CPU Version](#For-CPU-Version)
  * [For GPU Version](#For-GPU-Version)
* [Build and Run](#Build-and-Run)

***

# System requirements

- Ubuntu 18.04/20.04 or Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11
- (For GPU version) NVIDIA GPU capable of CUDA 11.2 and its drivers

# Prerequisite

## For Windows Machine

### Install WSL version 2

- Enter this command in an administrator PowerShell or Windows Command Prompt and then restarting your machine.

  ```bash
  wsl --install
  ```
- After restart, type this at PowerSehlll or Windows Command Prompt to confirm your WSL is set to version 2

  ```bash
  wsl --set-default-version 2
  ```
### Install Ubuntu 20.04 to WSL2

- Follow this link to install Ubuntu 20.04 at Microsoft Store
  - [Ubuntu 20.04 (Microsoft Store)](https://www.microsoft.com/store/productId/9N6SVWS3RX71)
  - Set username and password for the Ubuntu 20.04 while installation
- Type this at PowerShell or Windows Command Prompt to conform your Ubuntu 20.04 is running with WSL version 2

  ```bash
  wsl -v -l
  ```
- (Recommend) Install Windows Terminal to access Ubuntu in WSL2
  - [Windows Terminal (Microsoft Store)](https://www.microsoft.com/ko-kr/p/windows-terminal/9n0dx20hk701)

### (For GPU version) Install NVIDIA Grahics Driver for WSL2 Docker

- If you are running only with CPUs, you do not need this
- Download and install NVIDIA Driver for WSL2
  - [CUDA on Windows Subsystem for Linux (WSL)](https://developer.nvidia.com/cuda/tf_wsl)
- Check configuration for NVIDIA Graphics Card
  - Run this command inside Ubuntu 20.04 in WSL2

    ```bash
    glxinfo | grep OpenGL
    ```

    You should see something like following,

    ```bash
    OpenGL vendor string: Microsoft Corporation
    OpenGL renderer string: D3D12 (NVIDIA GeForce GTX 1660 Ti)
    OpenGL core profile version string: 3.3 (Core Profile) Mesa 21.0.3 - kisak-mesa PPA
    ```
    If not, do

    ```bash
    sudo add-apt-repository ppa:kisak/kisak-mesa && sudo apt-get update && sudo apt dist-upgrade
    ```

## For Ubuntu Machine
### (For GPU version) Set proprietrary NVIDIA graphics driver
- If you are running only with CPUs, you do not need this
- Choose `[proprietrary, tested]` driver on Additional Derivers at Software & Updates. For example, `nvidia-driver-460`
- To test the correct installation,

  ```
  nvidia-smi
  ```

# Install Docker

## For CPU version

- Docker installation

  ```bash
  sudo apt-get update
  sudo apt-get install \
      ca-certificates \
      curl \
      gnupg \
      lsb-release
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io
  sudo groupadd docker
  sudo usermod -aG docker $USER
  newgrp docker

  # If you are running on WSL2 at Windows machine
  # Run this command to autostart docker
  echo "[boot]\ncommand = service docker start" | sudo tee -a /etc/tf_wsl.conf
  ```

- To test docker, run this commands at a new terminal window

  ```bash
  # Test docker
  docker run hello-world

  # Test Tensorflow
  docker run -it tensorflow/tensorflow bash
  ```

## For GPU version

- Install docker following [CPU version installation above](https://github.com/Ship-Noise-Vibration-Lab/tensorflow_docker#for-cpu-version)

- Install NVIDIA docker container runtime

  ```bash
  curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
  curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list |\
      sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
  sudo apt-get update
  sudo apt-get install -y nvidia-container-runtime nvidia-docker2

  ```

  And restart docker

  ```bash
  sudo systemctl restart docker
  # If on WSL2 at Windows Machine
  sudo service docker restart
  ```

- Test docker with nvidia gpu

  ```bash
  docker run --gpus all nvidia/cuda:11.2.0-cudnn8-runtime-ubuntu20.04 nvidia-smi
  ```

  If you see something like this, it's a success

  ```bash
  +-----------------------------------------------------------------------------+
  | NVIDIA-SMI 460.91.03    Driver Version: 460.91.03    CUDA Version: 11.2     |
  |-------------------------------+----------------------+----------------------+
  | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
  | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
  |                               |                      |               MIG M. |
  |===============================+======================+======================|
  |   0  Quadro RTX 3000...  Off  | 00000000:01:00.0 Off |                  N/A |
  | N/A   77C    P0    65W /  N/A |   5054MiB /  5934MiB |     99%      Default |
  |                               |                      |                  N/A |
  +-------------------------------+----------------------+----------------------+

  +-----------------------------------------------------------------------------+
  | Processes:                                                                  |
  |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
  |        ID   ID                                                   Usage      |
  |=============================================================================|
  +-----------------------------------------------------------------------------+
  ```

- Test Tensorflow with gpu

  ```bash
  docker run --gpus all -it tensorflow/tensorflow:latest-gpu bash
  ```

- (Optional) For GPU status monitoring

  ```bash
  git clone https://github.com/Syllo/nvtop.git && cd nvtop
  sudo docker build --tag nvtop .
  sudo docker run -it --rm --runtime=nvidia --gpus=all --pid=host nvtop
  ```

# Pull Docker image from Docker Hub and run

- Add alias to `.bashrc` to run docker'd tensorflow easily

  ```bash
  # If CPU
  echo "tensorflow() { docker run -it --rm -v $PWD:/home/tf_docker/tf_ws -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) woensugchoi/tensorflow_docker:cpu python "$1" } | tee -a ~/.bashrc && source ~/.bashrc
  # If GPU
  echo "tensorflow() { docker run -it --rm -v $PWD:/home/tf_docker/tf_ws -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) woensugchoi/tensorflow_docker:gpu python "$1" } | tee -a ~/.bashrc && source ~/.bashrc
  ```

- Test with,

  ```bash
  tensorflow bash
  ```

  You should see something like this,

  ```bash
  ________                               _______________
  ___  __/__________________________________  ____/__  /________      __
  __  /  _  _ \_  __ \_  ___/  __ \_  ___/_  /_   __  /_  __ \_ | /| / /
  _  /   /  __/  / / /(__  )/ /_/ /  /   _  __/   _  / / /_/ /_ |/ |/ /
  /_/    \___//_/ /_//____/ \____//_/    /_/      /_/  \____/____/|__/

  You are running this container as user with ID 1000 and group 1000,
  which should map to the ID and group for your user on the Docker host. Great!

  tf_docker@f3922c96fc9c:~/tf_ws$
  ```

# (For Development) Build and Run

- Clone this repository

  ```bash
  mkdir -p ~/SNOVIL
  cd ~/SNOVIL
  git clone https://github.com/Ship-Noise-Vibration-Lab/tensorflow_docker.git
  ```

  This will clone the https://github.com/Ship-Noise-Vibration-Lab/tensorflow_docker into a directory `tensorflow_docker`

- Build Docker image (Upto 20 min)

  at the `Docker` directory where the Dockerfile is,

  ```bash
  cd ~/SNOVIL/tensorflow_docker
  # If CPU
  docker build -t tensorflow_docker -f ./TensorFlow_CPU.Dockerfile .
  # If GPU
  docker build -t tensorflow_docker -f ./TensorFlow_GPU.Dockerfile .
  ```

- Test

  at the directory where the python script is,

  ```bash
  # If CPU
  docker run -it --rm -v $PWD:/home/tf_docker/tf_ws -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker bash
  # If GPU
  docker run -it --rm --gpus all -v $PWD:/home/tf_docker/tf_ws -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker python  bash
  ```

  You should see something like this,

  ```bash
  ________                               _______________
  ___  __/__________________________________  ____/__  /________      __
  __  /  _  _ \_  __ \_  ___/  __ \_  ___/_  /_   __  /_  __ \_ | /| / /
  _  /   /  __/  / / /(__  )/ /_/ /  /   _  __/   _  / / /_/ /_ |/ |/ /
  /_/    \___//_/ /_//____/ \____//_/    /_/      /_/  \____/____/|__/

  You are running this container as user with ID 1000 and group 1000,
  which should map to the ID and group for your user on the Docker host. Great!

  tf_docker@f3922c96fc9c:~/tf_ws$

  ```

- Run Docker image with a python script

  at the directory where the python script is,

  ```bash
  # At directory where your python script is, (here it's Cylinder2D.py for example)
  # If CPU
  docker run -it --rm -v $PWD:/home/tf_docker/tf_ws -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker python ./Cylinder2D.py
  # If GPU
  docker run -it --rm --gpus all -v $PWD:/home/tf_docker/tf_ws -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker python ./Cylinder2D.py
  ```
