import json
import aws_cdk
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    SecretValue,
    Stack,
    aws_apigateway as apigw,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling
)
from constructs import Construct


ec2_type = "t2.micro"
key_name = "id_rsa"  # Setup key_name for EC2 instance login
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )  # Indicate your AMI, no need a specific id in the region
with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class SpringBootAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        #Deploy custom VPC
        vpc = ec2.Vpc(
        self, "CMS_vpc",
        cidr="10.0.0.0/16"
        )


        self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2
        )