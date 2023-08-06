#! /bin/bash
set -e

apt update -y
apt install -y software-properties-common ca-certificates dnsutils telnet unzip wget curl vim yamllint coreutils util-linux gawk rpm locales git python3-pip
ln -s /usr/bin/python3 /usr/bin/python 

# jq 1.6
curl -s --location -o jq https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64
chmod +x jq
mv jq /usr/bin

# yq
curl -s --location -o yq https://github.com/mikefarah/yq/releases/download/v4.9.6/yq_linux_amd64
chmod +x yq
mv yq /bin

# aws cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
  unzip awscliv2.zip && \
  ./aws/install && \
  rm -rf awscliv2.zip aws/

# github cli
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
  && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && apt update \
  && apt install gh -y

# hub
wget https://github.com/github/hub/releases/download/v2.14.2/hub-linux-amd64-2.14.2.tgz \
  && tar zxvf hub-linux-amd64-2.14.2.tgz \
  && ./hub-linux-amd64-2.14.2/install \
  && rm -rf hub-linux-amd64-2.14.2*

# update LC
locale-gen en_US.UTF-8

#=========== Clenaup ===========
rm -rf /var/lib/apt/lists/*
