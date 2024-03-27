import json
import boto3
import logging
import urllib.request
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Initialize the Secrets Manager client
    region_name = 'us-west-1' 
    client = boto3.client('ssm', region_name=region_name)
    print("hello")

    environment = ""
    print("Trying to run test")
    
    
    if 'ResourceProperties' in event and 'envn' in event['ResourceProperties']:
        environment = event['ResourceProperties']['envn']
    else:
        environment="development"
        print("Warning: 'ResourceProperties' or 'Environment' key not found in event object.")
    secret_prefix = f"/platform/account/{environment.lower()}/"  
    print(secret_prefix)
    secret_prefix = f"/platform/account/{environment.lower()}/"  

    try:
        # List all secrets, filter by name prefix
        response = client.describe_parameters(
         ParameterFilters=[
            {
               'Key': 'Name',
               'Option': 'BeginsWith',
               'Values': [secret_prefix]
          }
         ]
          )

        filtered_secrets = response['Parameters']

        secret_values = {}
        for secret in filtered_secrets:
            secret_name = secret['Name']
            parameters_secret = client.get_parameter(Name=secret_name,WithDecryption=True)
            get_secret_value_response = parameters_secret['Parameter']['Value']
            print("Secret Name ", secret_name, " Secret Value ", get_secret_value_response)

            secret_values[secret_name] = get_secret_value_response

        send_response(event, context, "SUCCESS", secret_values)

        return {
            'statusCode': 200,
            'body': json.dumps(secret_values)
        }
    except ClientError as e:
        print(e)
        send_response(event, context, "FAILED", {"error": "Failed to fetch secrets"})

        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Failed to fetch secrets"})
        }

def send_response(event, context, response_status, response_data):
    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name or context.invoked_function_arn,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": response_data
    })

    headers = {
        'Content-Type': '',
        'Content-Length': str(len(response_body))
    }

    request = urllib.request.Request(event['ResponseURL'], data=response_body.encode('utf-8'), headers=headers, method='PUT')
    with urllib.request.urlopen(request) as response:
        print("Status code:", response.getcode())
        print("Status message:", response.msg)
