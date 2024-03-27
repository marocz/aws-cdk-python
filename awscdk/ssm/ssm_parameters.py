import json
from aws_cdk import aws_ssm as ssm
from constructs import Construct
import os
from dotenv import load_dotenv
from aws_cdk import aws_lambda as lambda_, aws_iam as iam
from aws_cdk import aws_cloudformation as cfn
from aws_cdk import CustomResource

class SSMParameters:
    def __init__(self, stack: Construct, environment: str):

        config_file = f"./awscdk/ssm/env-{environment}.json"
        
        # Load the configuration from the file
        with open(config_file, 'r') as file:
            secrets = json.load(file)
        print("Loaded configuration:", secrets)
        
        for secret_key, secret_value in secrets.items():

            if secret_value:
                # Generate a parameter name
                parameter_name = f"/platform/account/{environment.lower()}/{secret_key.lower()}"

                # Create or update the SSM parameter
                ssm.StringParameter(stack, f"{environment}{secret_key}",
                                    parameter_name=parameter_name,
                                    string_value=secret_value,
                                    description=f"SSM parameter for {environment} environment, secret {secret_key.lower()}",
                                   )
