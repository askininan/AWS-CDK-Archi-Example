import json
import aws_cdk
from constructs import Construct
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_apigateway as apigw,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_cloudwatch as cw,
    aws_elasticloadbalancingv2 as elbv2,
)

from constructs import Construct

# Define EC2 instance configurations
ec2_type = "t2.micro"
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )
                                 
with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class awsCdkArchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Deploy custom VPC
        vpc = ec2.Vpc(
        self, "AWS-CDK-VPC",
        cidr="10.0.0.0/16")

        # Create ALB
        alb = elbv2.ApplicationLoadBalancer(self, "appALB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="appALB"
        )
        
        listener = alb.add_listener("port80",
                                    port=80,
                                    open=True)


        
        health_check = elbv2.HealthCheck(
            interval=aws_cdk.Duration.seconds(60),
            path="/health",
            timeout=aws_cdk.Duration.seconds(5)
        )
        
        # EC2 autoscaling group with one EC2 instance at start
        auto_scaling_g = autoscaling.AutoScalingGroup(self, "APP ASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=1,
                                                min_capacity=1,
                                                max_capacity=2,
        )

        # Second EC2 autoscaling group with one EC2 instance at start
        auto_scaling_g2 = autoscaling.AutoScalingGroup(self, "APP ASG2",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=1,
                                                min_capacity=1,
                                                max_capacity=2,
        )


        target_tracking_scaling_policy = autoscaling.TargetTrackingScalingPolicy(self, "TargetScalingPolicy",
            auto_scaling_group=auto_scaling_g,
            predefined_metric=autoscaling.PredefinedMetric.ASG_AVERAGE_CPU_UTILIZATION,
            target_value=80,
            cooldown=aws_cdk.Duration.minutes(20),
            disable_scale_in=False,
            estimated_instance_warmup=aws_cdk.Duration.minutes(20),
        )

        target_tracking_scaling_policy2 = autoscaling.TargetTrackingScalingPolicy(self, "TargetScalingPolicy2",
            auto_scaling_group=auto_scaling_g2,
            predefined_metric=autoscaling.PredefinedMetric.ASG_AVERAGE_CPU_UTILIZATION,
            target_value=80,
            cooldown=aws_cdk.Duration.minutes(20),
            disable_scale_in=False,
            estimated_instance_warmup=aws_cdk.Duration.minutes(20),
        )

        auto_scaling_g.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup1",
                             port=80,
                             targets=[auto_scaling_g, auto_scaling_g2]
        )

        CfnOutput(self, "Output",
                       value=alb.load_balancer_dns_name)