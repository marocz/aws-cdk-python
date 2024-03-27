import json
import pytest
import boto3
from unittest.mock import Mock
# from moto import mock_ssm
from unittest import TestCase
from ssm.secrets_function import lambda_handler  # Ensure this path is correct

def test_lambda_handler():

    # Prepare the Lambda event and context
    event = {
        "ResourceProperties": {
            "Environment": "development"
        },
        "RequestType": "Create",
        "ResponseURL": "https://webhook.site/79bfe7fa-099c-492c-90dc-c791029d5acf",
        "StackId": "arn:aws:cloudformation:us-west-2:example:stack/stack-name/guid",
        "RequestId": "unique id for this create request",
        "ResourceType": "Custom::TestResource",
        "LogicalResourceId": "MyTestResource",

       }

    mock_context = Mock()
    mock_context.log_stream_name = "test_log_stream"
    mock_context.invoked_function_arn = "test_function_arn"
    # Invoke the Lambda function
    response = lambda_handler(event, mock_context)

    # Check that the response contains the secret values and they are not null
    secrets = json.loads(response['body'])
    assert secrets.get("/platform/account/development/label") == "DevOps", "Secret value should not be null or missing"
    assert secrets.get("/platform/account/development/replicacount") == "1", "Secret value should not be null or missing"
    assert secrets.get("/platform/account/development/namespace") == "develop", "Secret value should not be null or missing"
