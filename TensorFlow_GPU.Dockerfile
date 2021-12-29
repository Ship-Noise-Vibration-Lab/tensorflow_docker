FROM tensorflow/tensorflow:latest-gpu-jupyter

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