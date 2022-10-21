FROM ubuntu:jammy-20221003

WORKDIR /workspace/
RUN mkdir Custom-Flower

COPY Graphs /workspace/Custom-Flower/Graphs
COPY Program /workspace/Custom-Flower/Program
COPY App /workspace/Custom-Flower/App

COPY tmux-script.sh /workspace/tmux-script.sh

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

RUN apt-get update && apt-get install -y \
  curl g++ make git tmux \
  libffi-dev libssl-dev libreadline-dev libbz2-dev liblzma-dev libsqlite3-dev python-tk python3-tk tk-dev \
  && rm -rf /var/lib/apt/lists/*

RUN cd /workspace/Custom-Flower/Program && mkdir -p bin && make prog && cp prog /workspace/Custom-Flower/App/prog
RUN cp /workspace/Custom-Flower/Graphs/Partitions/G0.2 /workspace/Custom-Flower/App/Partition.txt && cp /workspace/Custom-Flower/Graphs/ConvertedGraphs/G0.txt /workspace/Custom-Flower/App/Graph.txt

RUN curl https://pyenv.run | bash
RUN echo 'export PATH="/root/.pyenv/bin:$PATH"' >> /root/.bashrc && echo 'eval "$(pyenv init -)"' >> /root/.bashrc
RUN . /root/.bashrc && pyenv update && pyenv install 3.7.13 && pyenv virtualenv 3.7.13 flower-3.7.13 && echo flower-3.7.13 > Custom-Flower/.python-version
RUN . /root/.bashrc && cd Custom-Flower && python3 -m pip install -U pip && python3 -m pip install -U setuptools && pip install --retries 30 flwr torch torchvision
