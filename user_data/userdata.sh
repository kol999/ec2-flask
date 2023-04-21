#!/bin/bash 
#
#
yum install -y git tmux 
sudo -u ec2-user -i <<'EOF'
cd /home/ec2-user/

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py

TEMP_PEM="./temp.pem"
chmod 777 $TEMP_PEM
rm -rf $TEMP_PEM
mykey=$(aws ssm get-parameter --name my-irelandkey | jq .Parameter.Value | sed 's/\"//g' | sed 's/\\n/\n/g') 
echo "$mykey">$TEMP_PEM
chmod 400 $TEMP_PEM

# aws s3 sync s3://monday-gs-999/app/ /home/ec2-user/app/ 
git clone https://github.com/kol999/ec2-flask.git
cd /home/ec2-user/ec2-flask/flask-app
pip3 install -r requirements.txt 
python3 app.py
EOF
