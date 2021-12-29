FROM tensorflow/tensorflow:latest-jupyter

# Install some useful utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        sudo \
        nano \
        x11-apps \
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

# Add user
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} tf_docker \
 && useradd -ms /bin/bash tf_docker -g tf_docker

# Give sudo permission
RUN adduser --disabled-password --gecos "" tf_docker \
 && echo 'tf_docker:tf_docker' | chpasswd \
 && adduser user sudo \
 && echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
