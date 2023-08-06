FROM ubuntu:22.04

LABEL base="ubuntu:22.04"
LABEL description="infra-operator"

ENV SYSTEM_VERSION "ubuntu:22.04"

COPY ./install.sh install.sh
RUN bash install.sh && rm install.sh

COPY ./apps.sh apps.sh
RUN bash apps.sh && rm apps.sh

# fix unicode characters in string
ENV LANG=C.UTF-8

# export path, prow scripts mounted to /kaniko
ENV PATH=$PATH:/kaniko
# RUN echo "export PATH=$PATH:/kaniko" >> ~/.bashrc

WORKDIR /workspace/src

