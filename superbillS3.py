import boto3
import requests
from botocore.config import Config
import json

# This function capitalizes all text in the original object

def lambda_handler(event, context):
    event = json.loads(event)
    object_context = event["getObjectContext"]
    # Get the presigned URL to fetch the requested original object 
    # from S3
    s3_url = object_context["inputS3Url"]
    # Extract the route and request token from the input context
    request_route = object_context["outputRoute"]
    request_token = object_context["outputToken"]
    
    # Get the original S3 object using the presigned URL
    response = requests.get(s3_url)
    original_object = response.content.decode("utf-8")

    # Transform all text in the original object to uppercase
    # You can replace it with your custom code based on your use case
    transformed_object = original_object.upper()

    # Write object back to S3 Object Lambda
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
    # The WriteGetObjectResponse API sends the transformed data
    # back to S3 Object Lambda and then to the user
    s3.write_get_object_response(
        Body=transformed_object,
        RequestRoute=request_route,
        RequestToken=request_token)

    # Exit the Lambda function: return the status code  
    return {'status_code': 200}
    
class Context:
    def __init__(self):
        self.function_name = "test_function"
        self.memory_limit_in_mb = 128
        self.invoked_function_arn = "arn:aws:lambda:us-west-2:123456789012:function:test_function"
        self.aws_request_id = "test_request_id"
        
def main():
    
    s3_client = boto3.client('s3')
    bucket_name = 'super-bill-bucket'
    object_name = 'invoice_22.pdf'
    presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=3600)
    output_route = 's3://super-bill-bucket/text-bucket/'
    output_token = 'faketoken'
    
    request_example = '{'+'"getObjectContext": {'+'"inputS3Url": "'+presigned_url+'",'+'"outputRoute": "'+output_route+'",'+'"outputToken": "output-token"'+'}'+'}'

    context = Context
    #print(presigned_url)
    #print(request_example)

    print(lambda_handler(request_example, context))
main()
    
print(__name__)


