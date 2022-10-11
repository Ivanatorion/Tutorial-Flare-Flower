ARG PYTORCH_IMAGE=nvcr.io/nvidia/pytorch:22.04-py3
FROM ${PYTORCH_IMAGE}

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools
RUN python3 -m pip install torch torchvision tensorboard nvflare

WORKDIR /workspace/
RUN git clone https://github.com/NVIDIA/NVFlare.git
RUN echo "y" | poc -n 2
RUN mkdir -p poc/admin/transfer && cp -rf NVFlare/examples/* poc/admin/transfer

COPY tmux-script.sh /workspace/tmux-script.sh

RUN apt-get update && apt-get install -y \
  tmux \
  && rm -rf /var/lib/apt/lists/*

