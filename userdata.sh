#!/bin/bash 
#
#
sudo -u ec2-user -i <<'EOF'
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py
cd /home/ec2-user/
aws s3 sync s3://monday-gs-999/app/ /home/ec2-user/app/ 
cd /home/ec2-user/app 
pip3 install -r requirements.txt 
python3 app.py
EOF
