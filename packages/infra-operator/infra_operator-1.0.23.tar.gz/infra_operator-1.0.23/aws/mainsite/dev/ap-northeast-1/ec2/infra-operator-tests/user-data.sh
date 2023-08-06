#!/bin/bash
curl --version || yum install python-pip curl -y
aws --version || pip install awscli

REGION=`curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | awk '{ print substr($1, 1, length($1)-1) }'`
aws configure set default.region $REGION
aws configure set default.output text
IP_ADDRESS=`/opt/aws/bin/ec2-metadata -o | awk '{ print $2 }'`
INSTANCE_ID=`/opt/aws/bin/ec2-metadata -i | awk '{ print $2 }'`
HOST_NAME=`aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=Name" | cut -f 5`
hostnamectl set-hostname --static $HOST_NAME
echo "$IP_ADDRESS $HOST_NAME" >> /etc/hosts

touch ~/.disk_index
echo "IyEvYmluL2Jhc2gKbj0kKGNhdCB+Ly5kaXNrX2luZGV4KQpmb3IgaSBpbiAkKGxzYmxrIHwgYXdrICcvZGlzay97cHJpbnQgJDF9Jyk7IGRvCiAgaWYgWyAkKGZpbGUgLXMgL2Rldi8kaSB8IGF3ayAne3ByaW50ICQyfScpID0gImRhdGEiIF07IHRoZW4KICAgIG1rZGlyIC1wIC9zZXJ2ZXIkbgogICAgbWtmcy54ZnMgL2Rldi8kaQogICAgVVVJRD1gYmxraWQgfCBncmVwICRpIHwgYXdrIC1GICciJyAne3ByaW50ICQyfSdgCiAgICBlY2hvICJVVUlEPSRVVUlEICAgICAvc2VydmVyJG4gICAgICAgICAgIHhmcyAgICBkZWZhdWx0cyAgMCAgIDAiID4+IC9ldGMvZnN0YWIKICAgIG49JCgoJG4rMSkpCiAgICBlY2hvICRuID4gfi8uZGlza19pbmRleAogIGZpCmRvbmUKbW91bnQgLWEK" > ~/mount.sh
base64 -d ~/mount.sh | bash

# Install teleport service component
bash -c "$(curl --max-time 10 -fsSL https://static.iac.toolsfdg.net/_scripts/teleport/install.sh)"
