#!/usr/bin/env python3
import os

import aws_cdk as cdk

from asg_flask.asg_flask_stack import AsgFlaskStack
from asg_flask.cdk_vpc_stack import CdkVpcStack
from asg_flask.cdk_ec2_stack import CdkEc2Stack

app = cdk.App()
vpc_stack = CdkVpcStack(app, "cdk-vpc")
ec2_stack = CdkEc2Stack(app, "cdk-ec2", vpc=vpc_stack.vpc)

app.synth()
