FROM tensorflow/tensorflow:latest-gpu-jupyter

# Install some useful utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        sudo \
        nano \
        x11-apps \
        ssh \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip --no-cache-dir install --upgrade \
    pip setuptools matplotlib

# Install python3-qt for matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Add user and give sudo permission
RUN adduser --disabled-password --gecos "" tf_docker \
 && echo 'tf_docker:tf_docker' | chpasswd \
 && adduser tf_docker sudo \
 && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER tf_docker
