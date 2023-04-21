from aws_cdk import (
    Stack,
    aws_ec2 as ec2, 
    aws_elasticloadbalancingv2 as elb,
    aws_autoscaling as autoscaling,
    aws_iam as iam, 
    CfnOutput
)
from constructs import Construct

ec2_type = "t2.micro"
key_name = "kp-ireland"  # Setup key_name for EC2 instance login 
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )  # Indicate your AMI, no need a specific id in the region
with open("./user_data/userdata.sh") as f:
    user_data = f.read()


class CdkEc2Stack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Bastion
        bastion = ec2.BastionHostLinux(self, "myBastion",
                                       vpc=vpc,
                                       subnet_selection=ec2.SubnetSelection(
                                           subnet_type=ec2.SubnetType.PUBLIC),
                                       instance_name="myBastionHostLinux",
                                       instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))
        
        # Setup key_name for EC2 instance login if you don't use Session Manager
        # bastion.instance.instance.add_property_override("KeyName", key_name)

        bastion.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22), "Internet access SSH")

        # Create ALB
        alb = elb.ApplicationLoadBalancer(self, "myALB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="myALB"
                                          )
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 8000")
        listener = alb.add_listener("my8000",
                                    port=8000,
                                    open=True)


        ec2_role = iam.Role(self, "Ec2Role",
                            description="Give access to the apps on our EC2 instances",
                            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"),
                                              iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                                              iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMReadOnlyAccess")])

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                role=ec2_role, 
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                # block_devices=[
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/xvda",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_type=autoscaling.EbsDeviceVolumeType.GP2,
                                                #             volume_size=12,
                                                #             delete_on_termination=True
                                                #         )),
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/sdb",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_size=20)
                                                #         # 20GB, with default volume_type gp2
                                                #     )
                                                # ]
                                                )

        self.asg.connections.allow_from(alb, ec2.Port.tcp(8000), "ALB access 8000 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",
                             port=8000,
                             targets=[self.asg])


        self.asg.scale_on_cpu_utilization("cpu_scaling", target_utilization_percent=50)

        CfnOutput(self, "ALB_DNS", value=alb.load_balancer_dns_name)
