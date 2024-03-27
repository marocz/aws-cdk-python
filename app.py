#!/usr/bin/env python3
import os

import aws_cdk as cdk

from awscdk.aws_lambda import GetSSMLambda
from awscdk.awscdk_stack import AwscdkStack
from awscdk.eks_stack import CdkEKStack


app = cdk.App()

# Specify the environment as a command-line argument or modify as needed
env_USA = cdk.Environment(account="xxxxxxxx", region="us-west-1")
environment = app.node.try_get_context('environment')
AwscdkStack(app, "AwscdkStack", environment=environment)
CdkEKStack(app, "CdkEKStack", environment=environment,env=env_USA)
GetSSMLambda(app, "GetSSMLambda", environment=environment)

app.synth()
