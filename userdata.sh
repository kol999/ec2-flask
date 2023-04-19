#!/bin/bash 
#
#
yum install -y git tmux 
sudo -u ec2-user -i <<'EOF'
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py
cd /home/ec2-user/
# aws s3 sync s3://monday-gs-999/app/ /home/ec2-user/app/ 
git clone https://github.com/kol999/ec2-flask.git
cd /home/ec2-user/ec2-flask
pip3 install -r requirements.txt 
python3 app.py
EOF
