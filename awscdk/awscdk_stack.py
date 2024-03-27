from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)

from .ssm.ssm_parameters import SSMParameters

from constructs import Construct

class AwscdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment: str, **kwargs,) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SSMParameters(self, environment)
        # GetSSMParameters(self, environment)

        


