
from constructs import Construct
import os
from aws_cdk import aws_lambda as lambda_
from aws_cdk import Stack, aws_iam as iam
from aws_cdk import aws_cloudformation as cfn
from aws_cdk import CustomResource
from aws_cdk import aws_eks as eks

class GetSSMLambda(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment: str, **kwargs,) -> None:
        super().__init__(scope, construct_id, **kwargs)

        current_dir = os.path.dirname(__file__)

        # Path to the Lambda code directory
        lambda_code_path = os.path.join(current_dir, "lambda", "ssm")
        # Define the Lambda function
        lambda_role = iam.Role(self, "LambdaExecutionRole",
                               assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                               managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                                                 iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole')])
        print("in lambda function")
        lambda_role.add_to_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["secretsmanager:GetSecretValue", "secretsmanager:ListSecrets","ssm:DescribeParameters", "ssm:GetParameter", "ssm:GetParameters"],
        ))

        my_lambda = lambda_.Function(self, "SSMSecrets",
                                     runtime=lambda_.Runtime.PYTHON_3_8,
                                     handler="secrets_function.lambda_handler",
                                     code=lambda_.Code.from_asset(lambda_code_path),
                                     role=lambda_role)

        # Define the custom resource
        my_custom_resource = CustomResource(
            self, "SecretsResource",
            service_token=my_lambda.function_arn,
            properties={"envn": environment}  # Here you pass the environment variable to your Lambda
        )

        helm_values = {
            "controller": {
                "replicaCount": my_custom_resource.get_att_string("ReplicaCount"),
                "terminationGracePeriodSeconds": my_custom_resource.get_att_string("terminationGracePeriodSeconds"),
                "labels": {my_custom_resource.get_att_string("label"),my_custom_resource.get_att_string("namespace")}
            }
        }

        # Add the Helm chart to the cluster
        # eks.HelmChart(
        #     self, "NginxIngress",
        #     cluster_name="Cluster"
        #     chart="ingress-nginx",
        #     repository="https://kubernetes.github.io/ingress-nginx",
        #     namespace="ingress-nginx",
        #     values=helm_values
        # )