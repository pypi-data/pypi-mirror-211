#!/bin/sh

# To ensure nginx only start if config is pulled successfully.
set -ex

# Stop Nginx to ensure below step completed first.
systemctl stop nginx

# Install aws-cli
curl --version || yum install python-pip curl -y
aws --version || pip install awscli

# Setup hostname
REGION=`curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | awk '{ print substr($1, 1, length($1)-1) }'`
aws configure set default.region $REGION
aws configure set default.output text
IP_ADDRESS=`/opt/aws/bin/ec2-metadata -o | awk '{ print $2 }'`
INSTANCE_ID=`/opt/aws/bin/ec2-metadata -i | awk '{ print $2 }'`
SHORT_ID=`echo $INSTANCE_ID | cut -d"-" -f2`
HOST_NAME=`aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=Name" | cut -f 5`
hostnamectl set-hostname --static ""$HOST_NAME"_"$SHORT_ID""
echo "$IP_ADDRESS $HOST_NAME" >> /etc/hosts

# Clone Nginx Config
rm -rf /etc/nginx/*
git clone https://32e92739c0c78382b11a8c29dfa4156187fd925b@git.toolsfdg.net/devops/nginx-configs.git /server/nginx-configs
cp -r /server/nginx-configs/mainsite_dev/. /etc/nginx

## Get CDN IP Range
yum install -y jq
for i in `curl -s http://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips | jq '.[][]' -r`;do echo "set_real_ip_from " $i";";done > /etc/cloudfront_ip.conf

## Create log dir and update nginx config to use this log
LOG_DIR=/server/log/nginx/
mkdir -p $LOG_DIR

## Check Nginx config
/sbin/nginx -t -c /etc/nginx/nginx.conf

## Start and Enable Nginx
systemctl start nginx
systemctl enable nginx

## Fix log dir permission
chown -R www $LOG_DIR
chmod -R 755 $LOG_DIR

## Configure log rotation
yum install -y logrotate
echo ''"$LOG_DIR"'/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    sharedscripts
    postrotate
        [ ! -f /var/run/nginx.pid ] || kill -USR1 `cat /var/run/nginx.pid`
    endscript
}' > /etc/logrotate.d/nginx

# Node Exporter setup
sed -i 's/bijieprd/root/' /etc/systemd/system/node_exporter.service
systemctl daemon-reload
systemctl restart node_exporter.service