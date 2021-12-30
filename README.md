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
* [Install Alias](#Install-Alias)
* [Run Tensorflow](#Run-Tensorflow)

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
    ```

    If NOT, do

    ```bash
    sudo add-apt-repository ppa:kisak/kisak-mesa && sudo apt-get update && sudo apt dist-upgrade
    ```

### Important note for WSL2 in Windows Machine users
Using docker in WSL2 can eat up disk drive space very fast. It's becasue the expanded virtual drive of the WSL2 is not being reduced when it restarts. You may try pruning the docker images and containers. And compating the virtual disk size using diskpart.


## For Ubuntu Machine

### (For GPU version) Set proprietrary NVIDIA graphics driver

- If you are running only with CPUs, you do not need this
- Choose `[proprietrary, tested]` driver on Additional Derivers at Software & Updates. For example, `nvidia-driver-460` or `nvidia-driver-510`
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
  echo "[boot]\n command = service docker start" | sudo tee -a /etc/wsl.conf
  ```

- To test docker, run this commands at a new terminal window

  ```bash
  # Test docker
  sudo service docker start
  docker run hello-world
  ```

## For GPU version

- Install docker following [CPU version installation above](https://github.com/Ship-Noise-Vibration-Lab/tensorflow_docker#for-cpu-version)

- Install NVIDIA docker container runtime

  ```bash
  curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
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
  | NVIDIA-SMI 510.00       Driver Version: 510.06       CUDA Version: 11.6     |
  |-------------------------------+----------------------+----------------------+
  | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
  | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
  |                               |                      |               MIG M. |
  |===============================+======================+======================|
  |   0  NVIDIA GeForce ...  On   | 00000000:01:00.0  On |                  N/A |
  | 23%   55C    P0   108W / 260W |   1869MiB / 11264MiB |     N/A      Default |
  |                               |                      |                  N/A |
  +-------------------------------+----------------------+----------------------+

  +-----------------------------------------------------------------------------+
  | Processes:                                                                  |
  |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
  |        ID   ID                                                   Usage      |
  |=============================================================================|
  |  No running processes found                                                 |
  +-----------------------------------------------------------------------------+
  ```

- (Optional) For GPU status monitoring

  ```bash
  git clone https://github.com/Syllo/nvtop.git && cd nvtop
  sudo docker build --tag nvtop .
  sudo docker run -it --rm --runtime=nvidia --gpus=all --pid=host nvtop
  ```

# Install alias

## For bash
- Add alias to `.bashrc` to run docker'd tensorflow easily

  ```bash
  # If CPU
  wget https://raw.githubusercontent.com/Ship-Noise-Vibration-Lab/tensorflow_docker/main/sh_alias/sh_alias_CPU -P ~/ \
    && cat ~/sh_alias_CPU >> ~/.bashrc && rm ~/sh_alias_CPU && source ~/.bashrc
  # If GPU
  wget https://raw.githubusercontent.com/Ship-Noise-Vibration-Lab/tensorflow_docker/main/sh_alias/sh_alias_GPU -P ~/ \
    && cat ~/sh_alias_GPU >> ~/.bashrc && rm ~/sh_alias_GPU && source ~/.bashrc
  ```

## For zsh
- Add alias to `.zshrc` to run docker'd tensorflow easily

  ```bash
  # If CPU
  wget https://raw.githubusercontent.com/Ship-Noise-Vibration-Lab/tensorflow_docker/main/sh_alias/sh_alias_CPU -P ~/ \
    && cat ~/sh_alias_CPU >> ~/.zshrc && rm ~/sh_alias_CPU && source ~/.zshrc
  # If GPU
  wget https://raw.githubusercontent.com/Ship-Noise-Vibration-Lab/tensorflow_docker/main/sh_alias/sh_alias_GPU -P ~/ \
    && cat ~/sh_alias_GPU >> ~/.zshrc && rm ~/sh_alias_GPU && source ~/.zshrc
  ```

# Run Tensorflow

- Run tensorflow with,

  ```bash
  tensorflow_bash
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

  Type `exit` to exit from docker container

- How to use with your own tensorflow python scripts

  You can run any tensorflow python script with following command

  ```bash
  # if your tensorflow python script is myscript.py
  tensorflow myscript.py
  ```

## Note
- If you see warning message when running the script as follows,
  ```bash
  could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node
  Your kernel may have been built without NUMA support.
  ```

  Just ignore it. As long as you have msg like below at the end of those warnings, you should be ok.

  ```bash
  Created device /job:localhost/replica:0/task:0/device:GPU:0 with 8922 MB memory:
   -> device: 0, name: NVIDIA GeForce RTX 2080 Ti, pci bus id: 0000:01:00.0, compute capability: 7.5
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
  docker build -t tensorflow_docker:cpu -f ./Dockerfile/TensorFlow_CPU.Dockerfile .
  # If GPU
  docker build -t tensorflow_docker:gpu -f ./Dockerfile/TensorFlow_GPU.Dockerfile .
  ```

- Test

  at the directory where the python script is,

  ```bash
  # If CPU
  docker run -it --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --net=host \
      --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v $PWD:/home/tf_docker/tf_ws \
      -v ~/.ssh:/home/tf_docker/.ssh:ro \
      -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker:cpu bash
  # If GPU
  docker run -it --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --net=host \
      --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v $PWD:/home/tf_docker/tf_ws \
      -v ~/.ssh:/home/tf_docker/.ssh:ro --gpus all --runtime=nvidia \
      -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker:gpu bash
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
  # At directory where your python script is, (here it's `scripts/cnn_test.py` for example)
  # If CPU
  docker run -it --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --net=host \
      --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v $PWD:/home/tf_docker/tf_ws \
      -v ~/.ssh:/home/tf_docker/.ssh:ro \
      -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker:cpu \
      python scripts/cnn_test.py
  # If GPU
  docker run -it --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --net=host \
      --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v $PWD:/home/tf_docker/tf_ws \
      -v ~/.ssh:/home/tf_docker/.ssh:ro --gpus all --runtime=nvidia \
      -w /home/tf_docker/tf_ws -u $(id -u ${USER}):$(id -g ${USER}) tensorflow_docker:gpu \
      python scripts/cnn_test.py
  ```

# CPU vs Single GPU Benchmark

## Performance benchmark using cpu_vs_gpu.py for CNN training
- Setting
  ```bash
  _________________________________________________________________
  Layer (type)                Output Shape              Param #
  =================================================================
  input_1 (InputLayer)        [(None, 28, 28, 1)]       0
  conv2d (Conv2D)             (None, 28, 28, 32)        320
  max_pooling2d               (None, 14, 14, 32)        0
  conv2d_1 (Conv2D)           (None, 14, 14, 64)        18496
  max_pooling2d_1             (None, 7, 7, 64)          0
  conv2d_2 (Conv2D)           (None, 7, 7, 128)         73856
  max_pooling2d_2             (None, 4, 4, 128)         0
  flatten (Flatten)           (None, 2048)              0
  dense (Dense)               (None, 256)               524544
  dropout (Dropout)           (None, 256)               0
  dense_1 (Dense)             (None, 10)                2570
  ```

- CPU (Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz)

  ```bash
  Test loss: 0.02308735065162182
  Test accuracy: 0.991599977016449
  Computation time: 0:01:15.597915
  ```

- GPU (NVIDIA GeForce RTX 2080 Ti, with 8922 MB memory)

  ```bash
  Test loss: 0.021529724821448326
  Test accuracy: 0.9933000206947327
  Computation time: 0:00:21.897822
  ```

  About x4 with GPU for current case
