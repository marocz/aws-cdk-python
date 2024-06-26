import aws_cdk as core
import aws_cdk.assertions as assertions

from awscdk.awscdk_stack import AwscdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in awscdk/awscdk_stack.py
def test_aws_stack_created():
    app = core.App()
    stack = AwscdkStack(app, "awscdk")
    template = assertions.Template.from_stack(stack)
