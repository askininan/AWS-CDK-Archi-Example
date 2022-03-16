#!/usr/bin/env python3
import os

import aws_cdk as cdk

from AWS_CDK_ARCH.aws_cdk_arch_stack import awsCdkArchStack


app = cdk.App()
awsCdkArchStack(app, "awsCdkArchStack"),

app.synth()
