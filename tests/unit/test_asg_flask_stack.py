import aws_cdk as core
import aws_cdk.assertions as assertions

from asg_flask.asg_flask_stack import AsgFlaskStack

# example tests. To run these tests, uncomment this file along with the example
# resource in asg_flask/asg_flask_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AsgFlaskStack(app, "asg-flask")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
