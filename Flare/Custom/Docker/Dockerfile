ARG PYTORCH_IMAGE=nvcr.io/nvidia/pytorch:22.04-py3
FROM ${PYTORCH_IMAGE}

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools
RUN python3 -m pip install torch torchvision tensorboard nvflare

WORKDIR /workspace/
RUN git clone https://github.com/NVIDIA/NVFlare.git
RUN echo "y" | poc -n 2
RUN mkdir -p poc/admin/transfer && mkdir Custom-FLARE-Program && cp -rf NVFlare/examples/* poc/admin/transfer

COPY Graphs /workspace/Custom-FLARE-Program/Graphs
COPY Program /workspace/Custom-FLARE-Program/Program
COPY dist-search /workspace/Custom-FLARE-Program/dist-search

COPY dist-search /workspace/poc/admin/transfer/dist-search

COPY tmux-script.sh /workspace/tmux-script.sh

RUN apt-get update && apt-get install -y \
  tmux \
  && rm -rf /var/lib/apt/lists/*
  
RUN cd /workspace/Custom-FLARE-Program/Program && mkdir -p bin && make prog && cp prog /workspace/poc/site-1/prog && cp prog /workspace/poc/site-2/prog
RUN cp Custom-FLARE-Program/Graphs/ConvertedGraphs/G0.txt poc/server/Graph.txt && cp Custom-FLARE-Program/Graphs/Partitions/G0.2 poc/server/Partition.txt

